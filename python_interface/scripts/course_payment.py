import json, os
from web3 import Web3
from env_fp import private_key, rpc_url, adr_c, adr_r

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected()

account = w3.eth.account.from_key(private_key)
user_address = account.address

with open("../contract_abis/CoursePayment.json") as file:
    course_abi = json.load(file)

with open("../contract_abis/RefundManager.json") as file:
    refund_abi = json.load(file)

refund = w3.eth.contract(address=adr_r, abi=refund_abi)
course_address = refund.functions.getCourseAddress().call()
course = w3.eth.contract(
    address=Web3.to_checksum_address(course_address),
    abi=course_abi
)

def pay_course():
    has_access = course.functions.checkAccess().call()
    if has_access:
        print("Доступ вже надано. Оплата неможлива.")
        return

    amount_eth = float(input("Введіть суму (ETH): "))
    amount_wei = w3.to_wei(amount_eth, "ether")

    tx = course.functions.payForCourse().build_transaction({
        "from": user_address,
        "value": amount_wei,
        "gas": 200000,
        "gasPrice": w3.to_wei("1", "gwei"),
        "nonce": w3.eth.get_transaction_count(user_address),
        "chainId": 31337
    })

    signed = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Курс оплачено, хеш: {tx_hash.hex()}")


def check_access():
    access = course.functions.checkAccess().call()
    print("Доступ до курсу:", "Так" if access else "Ні")


def request_refund():
    print("Перевірка можливості повернення...")

    try:
        gas_estimate = refund.functions.refund().estimate_gas({
            "from": user_address
        })


        tx = refund.functions.refund().build_transaction({
            "from": user_address,
            "gas": int(gas_estimate * 1.2),
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(user_address),
            "chainId": w3.eth.chain_id
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"Очікування підтвердження транзакції...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            print(f"Повернення успішне! Хеш: {tx_hash.hex()}")
        else:
            print("Транзакція провалена в блокчейні.")
    except Exception as e:
        print(f"Помилка при оформленні повернення: {e}")

# Mеню
def main():
    while True:
        print("Меню")
        print("1. Оплатити курс")
        print("2. Перевірити доступ")
        print("3. Оформити повернення")
        print("0. Вийти")
        choice = input("Виберіть опцію: ")

        if choice == "1":
            pay_course()
        elif choice == "2":
            check_access()
        elif choice == "3":
            request_refund()
        elif choice == "0":
            break
        else:
            print("Невірний вибір")


if __name__ == "__main__":
    main()