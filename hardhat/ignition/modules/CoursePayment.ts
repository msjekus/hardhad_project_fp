import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("CoursePayment", (m) => {
  const CoursePayment = m.contract("CoursePayment");

  // m.call(counter, "incBy", [5n]);

  return { CoursePayment };
});