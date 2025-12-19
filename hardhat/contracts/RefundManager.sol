// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import "./CoursePayment.sol";

contract RefundManager {
    CoursePayment public course;
    uint256 public refundDeadline;

    event RefundProcessed(
        address indexed student,
        uint256 amount
    );

    constructor() {
        course = new CoursePayment();
        refundDeadline = block.timestamp + 1 days;
    }

    function refund() external {
        require(block.timestamp <= refundDeadline, "Refund period expired");
        require(course.checkAccess(), "No access");

        address student = course.student();
        uint256 amount = course.paidAmount();

        course.revokeAccess();

        (bool ok, ) = payable(student).call{value: amount}("");
        require(ok, "Refund failed");

        emit RefundProcessed(student, amount);
    }

    function getCourseAddress() external view returns (address) {
        return address(course);
    }
}

