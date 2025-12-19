import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("RefundManager", (m) => {
  const refundManager = m.contract("RefundManager");

  // m.call(counter, "incBy", [5n]);

  return { refundManager };
});