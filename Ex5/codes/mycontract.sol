pragma solidity >=0.4.22 <0.6.0;

contract BlockchainDebtManager {
    // 结构体定义债务，表示欠款金额
    struct Debt {
        uint32 balance;
    }

    // 用于存储债务信息的嵌套映射，outer address是债务人，inner address是债权人
    mapping(address => mapping(address => Debt)) internal debts;

    // 查询某债务人对某债权人的欠款金额
    function getDebt(address debtor, address creditor) public view returns (uint32) {
        return debts[debtor][creditor].balance;
    }

    // 增加债务记录
    function recordDebt(address creditor, uint32 amount, address[] memory cyclePath, uint32 cycleMin) public {
        address debtor = msg.sender;

        // 基础验证：不能自己借给自己，也不能为负值
        require(debtor != creditor, "Debtor and creditor cannot be the same.");
        require(amount > 0, "Debt amount must be positive.");

        Debt storage currentDebt = debts[debtor][creditor];

        // 如果不存在循环，直接增加债务
        if (cycleMin == 0) {
            currentDebt.balance = safeAdd(currentDebt.balance, amount);
            return;
        }

        // 验证循环路径和最小循环值
        require(cycleMin <= currentDebt.balance + amount, "Cycle minimum exceeds allowable debt.");
        require(validateAndAdjustCycle(creditor, debtor, cyclePath, cycleMin), "Invalid cycle path.");

        // 记录最终的债务值
        currentDebt.balance = safeAdd(currentDebt.balance, amount - cycleMin);
    }

    // 验证并调整循环路径
    function validateAndAdjustCycle(address start, address end, address[] memory path, uint32 cycleMin) private returns (bool) {
        if (start != path[0] || end != path[path.length - 1]) {
            return false;
        }

        // 限制路径长度
        if (path.length > 12) {
            return false;
        }

        // 遍历路径并调整循环内的债务值
        for (uint i = 1; i < path.length; i++) {
            Debt storage edgeDebt = debts[path[i - 1]][path[i]];
            if (edgeDebt.balance == 0 || edgeDebt.balance < cycleMin) {
                return false;
            }
            edgeDebt.balance -= cycleMin;
        }
        return true;
    }

    // 安全的加法操作，避免溢出
    function safeAdd(uint32 a, uint32 b) internal pure returns (uint32) {
        uint32 sum = a + b;
        require(sum >= a, "Addition overflow.");
        return sum;
    }
}
