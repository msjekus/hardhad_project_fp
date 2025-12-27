// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

//contract CoursePayment {
//    address public student;
//    uint256 public paidAmount;
//    bool public hasAccess;
//
//    event CoursePaid(address indexed student, uint256 amount);
//    event Refunded(address indexed student, uint256 amount);
//
//    function payForCourse() external payable {
//        require(!hasAccess, "Access already granted");
//        require(msg.value > 0, "Payment must be > 0");
//
//        student = msg.sender;
//        paidAmount = msg.value;
//        hasAccess = true;
//
//        emit CoursePaid(msg.sender, msg.value);
//    }
//
//    function checkAccess() external view returns (bool) {
//        return hasAccess;
//    }
//    function refundToStudent() external {
//        require(!hasAccess, "Access still active");
//        uint256 amount = paidAmount;
//        paidAmount = 0;
//
//        (bool ok, ) = payable(student).call{value: amount}("");
//        require(ok, "Refund transfer failed");
//    }
//
//    function refund() external {
//        require(hasAccess, "No active access");
//        require(msg.sender == student, "Not student");
//
//        hasAccess = true;
//        uint256 amount = paidAmount;
//        paidAmount = 0;
//
//        (bool ok, ) = payable(student).call{value: amount}("");
//        require(ok, "Refund failed");
//
//        emit Refunded(student, amount);
//    }
//}

contract CoursePayment {
    address public student;
    uint256 public paidAmount;
    bool public hasAccess;

    event CoursePaid(
        address indexed student,
        uint256 amount
    );
    event AccessRevoked(
        address indexed student
    );

    function payForCourse() external payable {
        require(!hasAccess, "Access already granted");
        require(msg.value > 0, "Payment must be > 0");

        student = msg.sender;
        paidAmount = msg.value;
        hasAccess = true;

        emit CoursePaid(msg.sender, msg.value);
    }
    function checkAccess() external view returns (bool) {
        return hasAccess;
    }

    function revokeAccess() external {
        require(hasAccess, "No active access");
        hasAccess = false;

        emit AccessRevoked(student);
    }
    function refundToStudent() external {
        require(!hasAccess, "Access still active");
        uint256 amount = paidAmount;
        paidAmount = 0;

        (bool ok, ) = payable(student).call{value: amount}("");
        require(ok, "Refund transfer failed");
    }
}

