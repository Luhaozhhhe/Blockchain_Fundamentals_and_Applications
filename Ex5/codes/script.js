// =============================================================================
//                                  Config 
// =============================================================================

// sets up web3.js
if (typeof web3 !== 'undefined')  {
	web3 = new Web3(web3.currentProvider);
} else {
	web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

// Default account is the first one
web3.eth.defaultAccount = web3.eth.accounts[0];
// Constant we use later
var GENESIS = '0x0000000000000000000000000000000000000000000000000000000000000000';

// This is the ABI for your contract (get it from Remix, in the 'Compile' tab)
// ============================================================
var abi = [
	{
		"constant": false,
		"inputs": [
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			},
			{
				"internalType": "uint32",
				"name": "amount",
				"type": "uint32"
			},
			{
				"internalType": "address[]",
				"name": "path",
				"type": "address[]"
			},
			{
				"internalType": "uint32",
				"name": "min_on_cycle",
				"type": "uint32"
			}
		],
		"name": "add_IOU",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"internalType": "address",
				"name": "debtor",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			}
		],
		"name": "lookup",
		"outputs": [
			{
				"internalType": "uint32",
				"name": "ret",
				"type": "uint32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
];

// ============================================================
abiDecoder.addABI(abi);
// call abiDecoder.decodeMethod to use this - see 'getAllFunctionCalls' for more

// Reads in the ABI
var BlockchainSplitwiseContractSpec = web3.eth.contract(abi);

// This is the address of the contract you want to connect to; copy this from Remix
var contractAddress = '0x68c49C93fA54a6691BE504cA2fBfca382b7de4B1'
//此处HASH通过REMIX复制后填入。按理说应该是每次编译完后的HASH都不一样，如果重新运行，需要重新填写。

var BlockchainSplitwise = BlockchainSplitwiseContractSpec.at(contractAddress)


// =============================================================================
//                            Functions To Implement 
// =============================================================================

// TODO: Add any helper functions here!
// Retrieves information from all calls in the block chain using the provided
// extractor. Extractor takes a single call as input and transforms it into
// a multiple values (a list), all of which are collected and de-duped.
// early_stop_fn is simply forward to getAllFunctionCalls.
// Helper function to handle all call data extraction
// 获取所有函数调用数据
function getCallData(extractor_fn, early_stop_fn = null) {
	const results = new Set();
	const all_calls = getAllFunctionCalls(contractAddress, 'add_IOU', early_stop_fn);
	all_calls.forEach(call => {
		extractor_fn(call).forEach(value => results.add(value));
	});
	return Array.from(results);
}

// 获取债权人列表
function getCreditors() {
	return getCallData(call => [call.args[0]]);
}

// 获取特定用户的所有债权人
function getCreditorsForUser(user) {
	return getCreditors().filter(creditor => BlockchainSplitwise.lookup(user, creditor).toNumber() > 0);
}

// 查找路径中的最小欠款金额
function findMinOnPath(path) {
	return path.slice(1).reduce((minOwed, debtor, i) => {
		const creditor = path[i];
		const amountOwed = BlockchainSplitwise.lookup(debtor, creditor).toNumber();
		return minOwed == null || minOwed > amountOwed ? amountOwed : minOwed;
	}, null);
}

// 获取系统中的所有用户（包括债务人和债权人）
function getUsers() {
	return getCallData(call => [call.from, call.args[0]]);
}

// 获取用户的总欠款金额
function getTotalOwed(user) {
	return getCreditors().reduce((totalOwed, creditor) => totalOwed + BlockchainSplitwise.lookup(user, creditor).toNumber(), 0);
}

// 获取用户的最后活动时间戳
function getLastActive(user) {
	const all_timestamps = getCallData(call => (call.from === user || call.args[0] === user) ? [call.timestamp] : []);
	return all_timestamps.length ? Math.max(...all_timestamps) : null;
}

// 向系统中添加一笔 IOU 记录
function add_IOU(creditor, amount) {
	const debtor = web3.eth.defaultAccount;
	const path = doBFS(creditor, debtor, getCreditorsForUser);

	if (path) {
		const min_on_cycle = Math.min(findMinOnPath(path), amount);
		return BlockchainSplitwise.add_IOU(creditor, amount, path, min_on_cycle);
	}
	return BlockchainSplitwise.add_IOU(creditor, amount, [], 0);
}



// =============================================================================
//                              Provided Functions 
// =============================================================================
// Reading and understanding these should help you implement the above

// This searches the block history for all calls to 'functionName' (string) on the 'addressOfContract' (string) contract
// It returns an array of objects, one for each call, containing the sender ('from'), arguments ('args')
// and timestamp (unix micros) of block collation ('timestamp').
// Stops retrieving function calls as soon as the earlyStopFn is found. earlyStop takes
// as input a candidate function call and must return a truth value.
// The chain is processed from head to genesis block.
function getAllFunctionCalls(addressOfContract, functionName, earlyStopFn) {
	var curBlock = web3.eth.blockNumber;
	var function_calls = [];
	while (curBlock !== GENESIS) {
	  var b = web3.eth.getBlock(curBlock, true);
	  var txns = b.transactions;
	  for (var j = 0; j < txns.length; j++) {
	  	var txn = txns[j];
	  	// check that destination of txn is our contract
	  	if (txn.to === addressOfContract.toLowerCase()) {
	  		var func_call = abiDecoder.decodeMethod(txn.input);
	  		// check that the function getting called in this txn is 'functionName'
	  		if (func_call && func_call.name === functionName) {
	  			var args = func_call.params.map(function (x) {return x.value});
	  			function_calls.push({
	  				from: txn.from,
	  				args: args,
	  				timestamp: b.timestamp,
	  			})
	  			if (earlyStopFn &&
	  					earlyStopFn(function_calls[function_calls.length-1])) {
	  				return function_calls;
	  			}
	  		}
	  	}
	  }
	  curBlock = b.parentHash;
	}
	return function_calls;
}

// We've provided a breadth-first search implementation for you, if that's useful
// It will find a path from start to end (or return null if none exists)
// You just need to pass in a function ('getNeighbors') that takes a node (string) and returns its neighbors (as an array)
function doBFS(start, end, getNeighbors) {
	var queue = [[start]];
	while (queue.length > 0) {
		var cur = queue.shift();
		var lastNode = cur[cur.length-1]
		if (lastNode === end) {
			return cur;
		} else {
			var neighbors = getNeighbors(lastNode);
			for (var i = 0; i < neighbors.length; i++) {
				queue.push(cur.concat([neighbors[i]]));
			}
		}
	}
	return null;
}
// =============================================================================
//                                      UI 
// =============================================================================

// This code updates the 'My Account' UI with the results of your functions
$("#total_owed").html("$"+getTotalOwed(web3.eth.defaultAccount));
$("#last_active").html(timeConverter(getLastActive(web3.eth.defaultAccount)));
$("#myaccount").change(function() {
	web3.eth.defaultAccount = $(this).val();
	$("#total_owed").html("$"+getTotalOwed(web3.eth.defaultAccount));
	$("#last_active").html(timeConverter(getLastActive(web3.eth.defaultAccount)))
});

// Allows switching between accounts in 'My Account' and the 'fast-copy' in 'Address of person you owe
var opts = web3.eth.accounts.map(function (a) { return '<option value="'+a+'">'+a+'</option>' })
$(".account").html(opts);
$(".wallet_addresses").html(web3.eth.accounts.map(function (a) { return '<li>'+a+'</li>' }))

// This code updates the 'Users' list in the UI with the results of your function
$("#all_users").html(getUsers().map(function (u,i) { return "<li>"+u+"</li>" }));

// This runs the 'add_IOU' function when you click the button
// It passes the values from the two inputs above
$("#addiou").click(function() {
  add_IOU($("#creditor").val(), $("#amount").val());
  window.location.reload(false); // refreshes the page after
});

// This is a log function, provided if you want to display things to the page instead of the JavaScript console
// Pass in a discription of what you're printing, and then the object to print
function log(description, obj) {
	$("#log").html($("#log").html() + description + ": " + JSON.stringify(obj, null, 2) + "\n\n");
}