from aiocryptopay import AioCryptoPay
from config import *


class CryptoBotPay():
    def __init__(self, cryptopay: AioCryptoPay):
        self.pay = cryptopay


    async def balance(self):
        balance = await self.pay.get_balance()
        await self.pay.close()
        return float(balance[0].available)


    async def create_check(self, amount):
        check = await self.pay.create_check(asset="USDT", amount=amount)
        await self.pay.close()
        return check
    

    async def send_cash(self, user, amount, hash):
        check = await self.pay.transfer(
            user, 
            asset="USDT", 
            amount=amount, 
            spend_id=hash
        )
        await self.pay.close()
        return check


    async def get_checks(self):
        payment = await self.pay.get_checks(status="active")
        await self.pay.close()
        return payment


    async def create_invoice(self, amount: float):
        invoice = await self.pay.create_invoice(amount, "USDT")
        await self.pay.close()
        return invoice

    async def pay_by_check(self, check_id: str, amount: float):
        """
        Выплата чеком.

        Args:
            check_id (str): ID чека.
            amount (float): Сумма выплаты.

        Returns:
            dict: Информация о транзакции.
        """
        try:
            payment = await self.pay.pay_check(check_id, amount, "USDT")
            await self.pay.close()
            return payment
        except Exception as e:
            print(f"Ошибка при выплате чеком: {e}")
            return None
