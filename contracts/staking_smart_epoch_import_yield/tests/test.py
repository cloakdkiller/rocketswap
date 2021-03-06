import unittest
from contracting.stdlib.bridge.time import Datetime

from contracting.client import ContractingClient


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.c = ContractingClient()
        self.c.flush()

        with open("../currency.s.py") as f:
            code = f.read()
            self.c.submit(code, name="currency", constructor_args={"vk": "sys"})
            self.c.submit(code, name="con_rswp", constructor_args={"vk": "sys"})

        self.currency = self.c.get_contract("currency")
        self.rswp = self.c.get_contract("con_rswp")

        with open("../con_basic_token.py") as f:
            code = f.read()
            self.c.submit(code, name="con_basic_token")

        self.basic_token = self.c.get_contract("con_basic_token")

        with open("con_staking_smart_epoch_import_yield.py") as f:
            code = f.read()
            self.c.submit(code, name="con_staking_smart_epoch")

        self.contract = self.c.get_contract("con_staking_smart_epoch")

        with open("con_staking_smart_epoch_compounding_import_yield_sa.py") as f:
            code = f.read()
            self.c.submit(code, name="con_staking_smart_epoch_single_asset")

        self.contract_single_asset = self.c.get_contract(
            "con_staking_smart_epoch_single_asset"
        )

        with open("../dex.py") as f:
            dex = f.read()
            self.c.submit(dex, "dex")

        self.dex = self.c.get_contract("dex")

        with open(
            "../liquidity_mining_smart_epoch/con_liquidity_mining_smart_epoch.py"
        ) as f:
            code = f.read()
            self.c.submit(code, name="con_liquidity_mining_smart_epoch")

        self.yield_farm = self.c.get_contract("con_liquidity_mining_smart_epoch")

        self.setupToken()

    def setupToken(self):
        # Approvals
        self.currency.approve(
            signer="bob", amount=999999999999, to="con_staking_smart_epoch"
        )
        self.currency.approve(
            signer="lucy", amount=999999999999, to="con_staking_smart_epoch"
        )
        self.currency.approve(
            signer="pete", amount=999999999999, to="con_staking_smart_epoch"
        )
        self.currency.approve(
            signer="janis", amount=999999999999, to="con_staking_smart_epoch"
        )
        self.currency.approve(
            signer="murray", amount=999999999999, to="con_staking_smart_epoch"
        )

        self.currency.approve(
            signer="con_staking_smart_epoch", amount=999999999999, to="bob"
        )
        self.currency.approve(
            signer="con_staking_smart_epoch", amount=999999999999, to="lucy"
        )
        self.currency.approve(
            signer="con_staking_smart_epoch", amount=999999999999, to="janis"
        )
        self.currency.approve(
            signer="con_staking_smart_epoch", amount=999999999999, to="murray"
        )
        self.currency.approve(
            signer="con_staking_smart_epoch", amount=999999999999, to="pete"
        )

        self.currency.approve(amount=999999999999, to="bob")
        self.currency.approve(amount=999999999999, to="janis")
        self.currency.approve(amount=999999999999, to="murray")
        self.currency.approve(amount=999999999999, to="pete")
        self.currency.approve(amount=999999999999, to="lucy")

        self.basic_token.approve(amount=99999999999, to="con_staking_smart_epoch")
        self.basic_token.approve(
            signer="con_staking_smart_epoch", amount=99999999999, to="bob"
        )
        self.basic_token.approve(
            signer="con_staking_smart_epoch", amount=99999999999, to="lucy"
        )
        self.basic_token.approve(
            signer="con_staking_smart_epoch", amount=99999999999, to="murray"
        )
        self.basic_token.approve(
            signer="con_staking_smart_epoch", amount=99999999999, to="janis"
        )
        self.basic_token.approve(
            signer="con_staking_smart_epoch", amount=99999999999, to="pete"
        )

        self.basic_token.transfer(to="con_staking_smart_epoch", amount=10000000)
        self.currency.transfer(to="bob", amount=1000)
        self.currency.transfer(to="lucy", amount=1000)
        self.currency.transfer(to="janis", amount=1000)
        self.currency.transfer(to="murray", amount=1000)
        self.currency.transfer(to="pete", amount=1000)

        self.contract.approve(signer="lucy", to="bob", amount=100000000)
        self.contract.approve(signer="bob", to="lucy", amount=100000000)
        self.contract.approve(
            signer="bob", to="con_staking_smart_epoch", amount=100000000
        )

        self.contract.setDevWallet(vk="dev_wallet")

    def tearDown(self):
        self.c.flush()

    def test_01_add_staking_tokens(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=100)

        bob_currency_balance = self.currency.balances["bob"]
        vault_currency_balance = self.currency.balances["con_staking_smart_epoch"]

        self.assertAlmostEqual(vault_currency_balance, 100)

        staked = self.contract.StakedBalance.get()
        self.assertAlmostEqual(staked, 100)

        current_epoch = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch, 1)

        deposit_record = self.contract.Deposits["bob"]
        self.assertAlmostEqual(deposit_record["amount"], 100)

        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=150)
        staked = self.contract.StakedBalance.get()
        self.assertAlmostEqual(staked, 250 + 3000 - 3000 / 10)

        current_epoch = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch, 2)

    def test_02_add_staking_tokens(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}

        with self.assertRaises(AssertionError):
            self.contract.addStakingTokens(
                environment=start_env, signer="bob", amount=10000
            )

        with self.assertRaises(AssertionError):
            self.contract.addStakingTokens(
                environment=start_env, signer="bob", amount=-100
            )

    def test_03_withdraw_yield(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=100)
        self.contract.withdrawYield(environment=env_2, signer="bob", amount=1500)

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 1350)

        dev_share = self.basic_token.balances["dev_wallet"]
        self.assertAlmostEqual(dev_share, 150)

        self.contract.withdrawYield(environment=env_2, signer="bob", amount=1500)

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 2700)

        dev_share = self.basic_token.balances["dev_wallet"]
        self.assertAlmostEqual(dev_share, 300)

        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(environment=env_2, signer="bob", amount=1500)

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 2700)

        dev_share = self.basic_token.balances["dev_wallet"]
        self.assertAlmostEqual(dev_share, 300)

        withdrawals_bob = self.contract.Withdrawals["bob"]
        self.assertAlmostEqual(withdrawals_bob, 3000)

        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 2700)

        dev_share = self.basic_token.balances["dev_wallet"]
        self.assertAlmostEqual(dev_share, 300)

        withdrawals_bob = self.contract.Withdrawals["bob"]
        self.assertAlmostEqual(withdrawals_bob, False)

    def test_04_withdraw_yield(self):

        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(signer="bob", amount=1500)

        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(signer="bob", amount=-1500)

    def test_05_withdraw_yield_and_stake(self):
        start_env = {"now": Datetime(year=2021, month=2, day=1)}
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}
        env_3 = {"now": Datetime(year=2021, month=2, day=1, hour=2)}

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=100)
        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(environment=env_3, signer="bob", amount=1500)

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 2700)

        dev_share = self.basic_token.balances["dev_wallet"]
        self.assertAlmostEqual(dev_share, 300)

        withdrawals_bob = self.contract.Withdrawals["bob"]
        self.assertAlmostEqual(withdrawals_bob, False)

    def test_06_multi_party_stake_and_withdraw_tokens_and_yield(self):
        start_env = {
            "now": Datetime(
                year=2021,
                month=2,
                day=1,
            )
        }
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}
        env_3 = {"now": Datetime(year=2021, month=2, day=1, hour=2)}
        env_4 = {"now": Datetime(year=2021, month=2, day=1, hour=4, minute=30)}
        env_5 = {"now": Datetime(year=2021, month=2, day=1, hour=6, minute=30)}

        self.contract.changeAmountPerHour(amount_per_hour=100)

        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 10)

        self.contract.addStakingTokens(environment=env_2, signer="janis", amount=5)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 15)

        self.contract.addStakingTokens(environment=env_3, signer="murray", amount=20)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 35)

        self.contract.addStakingTokens(environment=env_4, signer="pete", amount=100)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 135)

        self.contract.withdrawTokensAndYield(environment=env_5, signer="bob")
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 125)
        self.assertAlmostEqual(self.contract.Deposits["bob"], False)

        self.contract.withdrawTokensAndYield(environment=env_5, signer="janis")
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 120)
        self.assertAlmostEqual(self.contract.Deposits["janis"], False)

        self.contract.withdrawTokensAndYield(environment=env_5, signer="murray")
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(self.contract.Deposits["murray"], False)
        self.assertAlmostEqual(current_epoch["staked"], 100)

        self.contract.withdrawTokensAndYield(environment=env_5, signer="pete")
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 0)
        self.assertAlmostEqual(self.contract.Deposits["pete"], False)

        bob_token_balance = self.basic_token.balances["bob"]
        janis_token_balance = self.basic_token.balances["janis"]
        murray_token_balance = self.basic_token.balances["murray"]
        pete_token_balance = self.basic_token.balances["pete"]

        self.assertAlmostEqual(bob_token_balance, 252.9100529)
        self.assertAlmostEqual(janis_token_balance, 76.4550264)
        self.assertAlmostEqual(murray_token_balance, 172.4867724)
        self.assertAlmostEqual(pete_token_balance, 148.1481481)

        total = (
            bob_token_balance
            + janis_token_balance
            + murray_token_balance
            + pete_token_balance
        )
        vault_balance = self.basic_token.balances["con_staking_smart_epoch"]

        self.assertAlmostEqual(vault_balance + total, 10000000)

        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]

        self.assertAlmostEqual(current_epoch["staked"], 0)
        self.assertAlmostEqual(current_epoch_index, 9)

    def test_07_multi_party_stake_and_withdraw_yield(self):
        start_env = {
            "now": Datetime(
                year=2021,
                month=2,
                day=1,
            )
        }
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}
        env_3 = {"now": Datetime(year=2021, month=2, day=1, hour=2)}
        env_4 = {"now": Datetime(year=2021, month=2, day=1, hour=4, minute=30)}
        env_5 = {"now": Datetime(year=2021, month=2, day=1, hour=6, minute=30)}

        self.contract.changeAmountPerHour(amount_per_hour=100)

        self.contract.setDevRewardPct(amount=0)

        # self.contract.setEmissionRatePerHour(amount=100)
        # self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="janis", amount=5)
        self.contract.addStakingTokens(environment=env_3, signer="murray", amount=20)
        self.contract.addStakingTokens(environment=env_4, signer="pete", amount=100)

        self.contract.withdrawYield(
            environment=env_5, signer="bob", amount=1009299299299
        )
        self.contract.withdrawYield(environment=env_5, signer="janis", amount=100000000)
        self.contract.withdrawYield(
            environment=env_5, signer="murray", amount=100000000
        )
        self.contract.withdrawYield(environment=env_5, signer="pete", amount=100000000)

        bob_token_balance = self.basic_token.balances["bob"]
        janis_token_balance = self.basic_token.balances["janis"]
        murray_token_balance = self.basic_token.balances["murray"]
        pete_token_balance = self.basic_token.balances["pete"]

        bob_expected_amount = 252.9100529
        janis_expected_amount = 76.4550264
        murray_expected_amount = 172.4867724
        pete_expected_amount = 148.1481481

        self.assertAlmostEqual(bob_token_balance, bob_expected_amount)
        self.assertAlmostEqual(janis_token_balance, janis_expected_amount)
        self.assertAlmostEqual(murray_token_balance, murray_expected_amount)
        self.assertAlmostEqual(pete_token_balance, pete_expected_amount)

        bob_withdrawn = self.contract.Withdrawals["bob"]
        janis_withdrawn = self.contract.Withdrawals["janis"]
        murray_withdrawn = self.contract.Withdrawals["murray"]
        pete_withdrawn = self.contract.Withdrawals["pete"]

        self.assertAlmostEqual(bob_withdrawn, bob_expected_amount)
        self.assertAlmostEqual(janis_withdrawn, janis_expected_amount)
        self.assertAlmostEqual(murray_withdrawn, murray_expected_amount)
        self.assertAlmostEqual(pete_withdrawn, pete_expected_amount)

        total = (
            bob_token_balance
            + janis_token_balance
            + murray_token_balance
            + pete_token_balance
        )
        vault_balance = self.basic_token.balances["con_staking_smart_epoch"]

        self.assertAlmostEqual(vault_balance + total, 10000000)

        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]

        self.assertAlmostEqual(current_epoch_index, 5)
        self.assertAlmostEqual(current_epoch["staked"], 135)

    def test_08_multi_party_stake_and_withdraw_yield_then_withdraw_tokens_and_yield(
        self,
    ):
        start_env = {
            "now": Datetime(
                year=2021,
                month=2,
                day=1,
            )
        }
        env_2 = {"now": Datetime(year=2021, month=2, day=1, hour=1)}
        env_3 = {"now": Datetime(year=2021, month=2, day=1, hour=2)}
        env_4 = {"now": Datetime(year=2021, month=2, day=1, hour=4, minute=30)}
        env_5 = {"now": Datetime(year=2021, month=2, day=1, hour=6, minute=30)}

        self.contract.changeAmountPerHour(amount_per_hour=100)
        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=start_env, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="janis", amount=5)
        self.contract.addStakingTokens(environment=env_3, signer="murray", amount=20)
        self.contract.addStakingTokens(environment=env_4, signer="pete", amount=100)

        self.contract.withdrawYield(
            environment=env_5, signer="bob", amount=1009299299299
        )
        self.contract.withdrawYield(environment=env_5, signer="janis", amount=100000000)
        self.contract.withdrawYield(
            environment=env_5, signer="murray", amount=100000000
        )
        self.contract.withdrawYield(environment=env_5, signer="pete", amount=100000000)

        current_epoch_index = self.contract.CurrentEpochIndex.get()
        current_epoch = self.contract.Epochs[current_epoch_index]
        # print(current_epoch['staked'])
        self.assertAlmostEqual(current_epoch_index, 5)
        self.assertAlmostEqual(current_epoch["staked"], 135)

        self.contract.withdrawTokensAndYield(environment=env_5, signer="bob")
        self.contract.withdrawTokensAndYield(environment=env_5, signer="janis")
        self.contract.withdrawTokensAndYield(environment=env_5, signer="murray")
        self.contract.withdrawTokensAndYield(environment=env_5, signer="pete")

        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 9)

        bob_token_balance = self.basic_token.balances["bob"]
        janis_token_balance = self.basic_token.balances["janis"]
        murray_token_balance = self.basic_token.balances["murray"]
        pete_token_balance = self.basic_token.balances["pete"]

        bob_expected_amount = 252.9100529
        janis_expected_amount = 76.4550264
        murray_expected_amount = 172.4867724
        pete_expected_amount = 148.1481481

        self.assertAlmostEqual(bob_token_balance, bob_expected_amount)
        self.assertAlmostEqual(janis_token_balance, janis_expected_amount)
        self.assertAlmostEqual(murray_token_balance, murray_expected_amount)
        self.assertAlmostEqual(pete_token_balance, pete_expected_amount)

        total = (
            bob_token_balance
            + janis_token_balance
            + murray_token_balance
            + pete_token_balance
        )
        vault_balance = self.basic_token.balances["con_staking_smart_epoch"]

        self.assertAlmostEqual(vault_balance + total, 10000000)

        current_epoch = self.contract.Epochs[current_epoch_index]
        self.assertAlmostEqual(current_epoch["staked"], 0)

        bob_deposits = self.contract.Deposits["bob"]
        janis_deposits = self.contract.Deposits["janis"]
        murray_deposits = self.contract.Deposits["murray"]
        pete_deposits = self.contract.Deposits["pete"]

        self.assertAlmostEqual(bob_deposits, False)
        self.assertAlmostEqual(janis_deposits, False)
        self.assertAlmostEqual(murray_deposits, False)
        self.assertAlmostEqual(pete_deposits, False)

    def test_09_recover_yield_token(self):
        self.assertAlmostEqual(
            self.basic_token.balances["con_staking_smart_epoch"], 10000000
        )
        self.contract.recoverYieldToken()
        self.assertAlmostEqual(self.basic_token.balances["con_staking_smart_epoch"], 0)

    def test_09a_recover_yield_token(self):
        self.assertAlmostEqual(
            self.basic_token.balances["con_staking_smart_epoch"], 10000000
        )
        self.contract.recoverYieldToken()
        self.assertAlmostEqual(self.basic_token.balances["con_staking_smart_epoch"], 0)

    def test_10_start_time(self):
        env_1 = {"now": Datetime(year=2020, month=2, day=1)}
        env_2 = {"now": Datetime(year=2021, month=2, day=1)}

        self.contract.setStartTime(year=2022, month=1, day=1, hour=0)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(environment=env_2, signer="bob", amount=1500)

    def test_11_set_time_methods(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        self.contract.setStartTime(year=2021, month=1, day=1, hour=1)
        self.contract.setEndTime(year=2021, month=1, day=1, hour=1)

        start_time = self.contract.StartTime.get()
        end_time = self.contract.EndTime.get()

        self.assertAlmostEqual(Datetime(year=2021, month=1, day=1, hour=1), start_time)
        self.assertAlmostEqual(Datetime(year=2021, month=1, day=1, hour=1), end_time)

    def test_12_start_time(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}

        # self.contract.setStartTime(year=2021, month=1, day=1, hour=1)
        # self.contract.setEndTime(year=2023, month=1, day=1, hour=1)

        self.contract.changeAmountPerHour(amount_per_hour=100)
        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="janis", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="murray", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="pete", amount=10)

        self.contract.withdrawYield(
            environment=env_2, signer="bob", amount=1009299299299
        )

        self.assertAlmostEqual(self.basic_token.balances["bob"], 25)
        self.contract.withdrawTokensAndYield(signer="bob")

    def test_13_end_time(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=3)}

        self.contract.setStartTime(year=2021, month=1, day=1, hour=1)
        self.contract.setEndTime(year=2021, month=1, day=1, hour=2)

        self.contract.changeAmountPerHour(amount_per_hour=100)
        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="janis", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="murray", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="pete", amount=10)

        self.contract.withdrawYield(
            environment=env_2, signer="bob", amount=1009299299299
        )
        self.contract.withdrawYield(environment=env_2, signer="janis", amount=100000000)
        self.contract.withdrawYield(
            environment=env_2, signer="murray", amount=100000000
        )
        self.contract.withdrawYield(environment=env_2, signer="pete", amount=100000000)

        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")
        self.contract.withdrawTokensAndYield(environment=env_2, signer="janis")
        self.contract.withdrawTokensAndYield(environment=env_2, signer="murray")
        self.contract.withdrawTokensAndYield(environment=env_2, signer="pete")

        self.assertAlmostEqual(self.basic_token.balances["bob"], 25)
        self.assertAlmostEqual(self.basic_token.balances["janis"], 25)
        self.assertAlmostEqual(self.basic_token.balances["murray"], 25)
        self.assertAlmostEqual(self.basic_token.balances["pete"], 25)

    def test_14_addStakingTokens_check_amount_should_pass(self):

        self.contract.addStakingTokens(signer="bob", amount=10)
        self.contract.addStakingTokens(signer="bob", amount=10)

        deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(deposits["amount"], 20)

    def test_15_addStakingTokens_check_amount_should_fail(self):

        self.contract.addStakingTokens(signer="bob", amount=10)
        self.contract.addStakingTokens(signer="bob", amount=10)
        self.contract.addStakingTokens(signer="bob", amount=10)

        deposits = self.contract.Deposits["bob"]

        with self.assertRaises(AssertionError):
            self.assertAlmostEqual(deposits["amount"], 20)

    def test_16_addStakingTokens_withdrawTokensAndYield_check_len_should_pass(self):

        self.contract.addStakingTokens(signer="bob", amount=10)
        self.contract.addStakingTokens(signer="bob", amount=10)

        self.contract.withdrawTokensAndYield(signer="bob")
        deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(deposits, False)

    def test_17_emergencyReturnStake(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=3)}

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        self.contract.withdrawYield(environment=env_2, signer="bob", amount=1500)

        self.contract.emergencyReturnStake(environment=env_2, signer="bob")
        deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(deposits, False)

        withdrawals = self.contract.Withdrawals["bob"]
        self.assertAlmostEqual(withdrawals, 0)

        bob_balance = self.currency.balances["bob"]
        self.assertAlmostEqual(bob_balance, 1000)

        with self.assertRaises(AssertionError):
            self.assertAlmostEqual(bob_balance, 0)

    def test_18_epoch_incrementing_over_time(self):
        # Testing that the Epoch will not increment unless the decided time has elapsed.
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=0, minute=15)}
        env_3 = {"now": Datetime(year=2021, month=1, day=1, hour=0, minute=30)}
        env_4 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}

        self.contract.changeAmountPerHour(amount_per_hour=100)
        self.contract.setDevRewardPct(amount=0)

        current_epoch_idx = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_idx, 1)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="janis", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="murray", amount=10)
        self.contract.addStakingTokens(environment=env_1, signer="pete", amount=10)

        current_epoch_idx = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_idx, 5)

        min_seconds = 60 * 60
        self.contract.setEpochMinTime(environment=env_2, min_seconds=min_seconds)

        # This one gets skipped / doesn't increment the epoch.
        self.contract.addStakingTokens(environment=env_1, signer="pete", amount=10)

        current_epoch_idx = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_idx, 5)

        self.contract.addStakingTokens(environment=env_4, signer="pete", amount=10)

        current_epoch_idx = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_idx, 6)

        staked_balance = self.contract.StakedBalance.get()
        self.assertAlmostEqual(staked_balance, 110)

        current_epoch = self.contract.Epochs[current_epoch_idx]
        current_epoch_staked_balance = current_epoch["staked"]
        self.assertAlmostEqual(current_epoch_staked_balance, 110)

    def test_19_epoch_incrementing_when_max_ratio_exceeded_addStakingTokens(self):
        # all of the below test occurs within the min epoch time
        # will only increment when the maxRatioIncrease is exceeded.
        self.contract.setEpochMinTime(min_seconds=60 * 60)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)
        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)

        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 2)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 3)

        # skips
        self.contract.addStakingTokens(signer="bob", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 3)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=20)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 4)

        # skips
        self.contract.addStakingTokens(signer="bob", amount=20)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 4)

    def test_20_epoch_incrementing_when_max_ratio_exceeded_withdrawTokensAndYield(self):
        # all of the below test occurs within the min epoch time
        # will only increment when the maxRatioIncrease is exceeded.
        self.contract.setEpochMinTime(min_seconds=60 * 60)
        self.contract.setEpochMaxRatioIncrease(ratio=0.1)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 2)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 3)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=3)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 4)

        # skips
        self.contract.addStakingTokens(signer="bob", amount=3)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 4)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=1)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 5)

    def test_21_epoch_incrementing_when_max_ratio_exceeded_withdrawTokensAndYield(self):
        # all of the below test occurs within the min epoch time
        # will only increment when the maxRatioIncrease is exceeded.
        self.contract.setEpochMinTime(min_seconds=60 * 60)
        self.contract.setEpochMaxRatioIncrease(ratio=0.1)

        # increments
        self.contract.addStakingTokens(signer="bob", amount=100)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 1)

        # print(self.contract.Epochs[2])
        # {'time': 2021-04-21 17:16:00, 'staked': 100, 'amt_per_hr': 3000}

        # increments
        self.contract.addStakingTokens(signer="janis", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 2)
        # print(self.contract.Epochs[2])
        # {'time': 2021-04-21 17:19:00, 'staked': 110, 'amt_per_hr': 3000}

        # skip
        self.contract.addStakingTokens(signer="janis", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 2)
        # print(self.contract.Epochs[2])
        # {'time': 2021-04-21 17:19:00, 'staked': 110, 'amt_per_hr': 3000}

        # increments
        self.contract.addStakingTokens(signer="janis", amount=10)
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        self.assertAlmostEqual(current_epoch_index, 3)
        print(self.contract.Epochs[3])
        # {'time': 2021-04-21 17:33:00, 'staked': 130, 'amt_per_hr': 3000}

        # increments
        self.contract.withdrawTokensAndYield(signer="janis")
        current_epoch_index = self.contract.CurrentEpochIndex.get()
        # print(self.contract.StakedBalance.get())
        print(self.contract.Epochs[4])
        # self.assertAlmostEqual(current_epoch_index, 2)
        self.assertAlmostEqual(current_epoch_index, 4)

    def test_21_time_ramps_lookup(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=11)}
        env_3 = {"now": Datetime(year=2021, month=1, day=21)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

        bob_token_balance = self.basic_token.balances["bob"]

        self.assertAlmostEqual(bob_token_balance, 72000)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.changeAmountPerHour(environment=env_2, amount_per_hour=3000)
        self.contract.withdrawTokensAndYield(environment=env_3, signer="bob")

        bob_token_balance = self.basic_token.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 288000)

    def test_22_time_ramps_exceed_range(self):
        env_1 = {"now": Datetime(year=2021, month=1, day=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=4)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setTimeRampValues(
            data=[
                {"lower": 0, "upper": 1, "multiplier": 0},
                {"lower": 1, "upper": 2, "multiplier": 1},
            ]
        )
        self.contract.setDevRewardPct(amount=0)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

        bob_token_balance = self.basic_token.balances["bob"]

        self.assertAlmostEqual(bob_token_balance, 216000)

    def test_23_time_ramps_carry_to_new_deposit(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=11, hour=0)}
        env_3 = {"now": Datetime(year=2021, month=1, day=21, hour=0)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)

        bob_deposits = self.contract.Deposits["bob"]
        print(bob_deposits)

        # expected balance =
        # Epoch 1 - 10 days // time_step_multiplier = 0.1
        # (10 x 24 x 10 = 2400 * 0.1) + 20
        # = 260

        self.assertAlmostEqual(bob_deposits["amount"], 260)

        # increment epoch
        self.contract.addStakingTokens(environment=env_3, signer="bob", amount=0)
        bob_deposits = self.contract.Deposits["bob"]

        # expected balance =
        # Epoch 1 - 260
        # Epoch 2 - 3 // 10 days // time_step_multiplier = 0.3
        # (10 x 24 x 10 = 2400 * 0.2) + 260

        self.assertAlmostEqual(bob_deposits["amount"], 740)

    def test_23a_time_ramps_give_appropriate_yield(self):

        env_0 = {"now": Datetime(year=2021, month=12, day=31, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=2, hour=0)}
        env_3 = {"now": Datetime(year=2021, month=1, day=3, hour=0)}
        env_4 = {"now": Datetime(year=2021, month=1, day=4, hour=0)}
        env_5 = {"now": Datetime(year=2021, month=1, day=5, hour=0)}
        env_6 = {"now": Datetime(year=2021, month=1, day=6, hour=0)}
        env_7 = {"now": Datetime(year=2021, month=1, day=7, hour=0)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setTimeRampValues(data =
            [
                {"lower": 0, "upper": 1, "multiplier": 0.1},
                {"lower": 1, "upper": 2, "multiplier": 0.2},
                {"lower": 2, "upper": 3, "multiplier": 0.3},
                {"lower": 3, "upper": 4, "multiplier": 0.4},
                {"lower": 4, "upper": 5, "multiplier": 0.5},
                {"lower": 10, "upper": 100, "multiplier": 1},
            ]
        )
        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        # deposit amount = 10
        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        # deposit amount = 
        # 10 + (10 * 24) * 0.2 + 10 = 44
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 68)

        # deposit amount = 68
        # yield due = 68 + (10 * 24) * 0.3 + 10
        self.contract.addStakingTokens(environment=env_3, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 150)

        # deposit amount = 150
        # yield due = 150 + (10 * 24) * 0.4 + 10
        self.contract.addStakingTokens(environment=env_4, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 256)

        # deposit amount = 256
        # yield due = 256 + (10 * 24) * 0.5 + 10
        self.contract.addStakingTokens(environment=env_5, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 386)

        # deposit amount = 386
        # yield due = 386 + (10 * 24) * 1 + 10
        self.contract.addStakingTokens(environment=env_6, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 636)

        # deposit amount = 636
        # yield due = 636 + (10 * 24) * 1 + 10
        self.contract.addStakingTokens(environment=env_7, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 886)

    def test_23b_time_ramps_gives_right_level_when_multiple_deposits_before_start_date(self):

        env_0 = {"now": Datetime(year=2020, month=12, day=31, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=2, hour=0)}
        env_3 = {"now": Datetime(year=2021, month=1, day=3, hour=0)}
        env_4 = {"now": Datetime(year=2021, month=1, day=4, hour=0)}
        env_5 = {"now": Datetime(year=2021, month=1, day=5, hour=0)}
        env_6 = {"now": Datetime(year=2021, month=1, day=6, hour=0)}
        env_7 = {"now": Datetime(year=2021, month=1, day=7, hour=0)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setStartTime(year=2021, month=1, day=1, hour=0)
        self.contract.setTimeRampValues(data =
            [
                {"lower": 0, "upper": 1, "multiplier": 0.1},
                {"lower": 1, "upper": 2, "multiplier": 0.2},
                {"lower": 2, "upper": 3, "multiplier": 0.3},
                {"lower": 3, "upper": 4, "multiplier": 0.4},
                {"lower": 4, "upper": 5, "multiplier": 0.5},
                {"lower": 10, "upper": 100, "multiplier": 1},
            ]
        )
        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        # deposit amount = 5
        self.contract.addStakingTokens(environment=env_0, signer="bob", amount=5)

        # deposit amount = 10
        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=5)

        # deposit amount = 
        # 10 + (10 * 24) * 0.2 + 10 = 44
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 68)

    def test_23c_time_ramps_gives_right_level_when_deposit_before_start_date(self):

        env_0 = {"now": Datetime(year=2020, month=12, day=31, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=2, hour=0)}
        env_3 = {"now": Datetime(year=2021, month=1, day=3, hour=0)}
        env_4 = {"now": Datetime(year=2021, month=1, day=4, hour=0)}
        env_5 = {"now": Datetime(year=2021, month=1, day=5, hour=0)}
        env_6 = {"now": Datetime(year=2021, month=1, day=6, hour=0)}
        env_7 = {"now": Datetime(year=2021, month=1, day=7, hour=0)}

        self.contract.toggleTimeRamp(on=True)
        self.contract.setStartTime(year=2021, month=1, day=1, hour=0)
        self.contract.setTimeRampValues(data =
            [
                {"lower": 0, "upper": 1, "multiplier": 0.1},
                {"lower": 1, "upper": 2, "multiplier": 0.2},
                {"lower": 2, "upper": 3, "multiplier": 0.3},
                {"lower": 3, "upper": 4, "multiplier": 0.4},
                {"lower": 4, "upper": 5, "multiplier": 0.5},
                {"lower": 10, "upper": 100, "multiplier": 1},
            ]
        )
        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        # deposit amount = 5
        self.contract.addStakingTokens(environment=env_0, signer="bob", amount=10)


        # deposit amount = 
        # 10 + (10 * 24) * 0.2 + 10 = 44
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 68)


    def test_24_compounding_gives_correct_deposit_balance(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_3 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        # bob deposit = 10 + 10 + 10
        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 30)
        self.contract.addStakingTokens(environment=env_3, signer="bob", amount=10)

        bob_deposits = self.contract.Deposits["bob"]
        self.assertAlmostEqual(bob_deposits["amount"], 50)

    def test_25_test_date(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}
        # env_3 = {"now": Datetime(year=2021, month=5, day=1, hour=2)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        # bob deposit = 10 + 10 + 10
        bob_deposits = self.contract.Deposits["bob"]
        print(str(bob_deposits["step_offset"]))

    def test_26_withdraw_after_compound_fails(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=5, day=1, hour=0)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)
        self.contract.addStakingTokens(environment=env_2, signer="bob", amount=10)
        bob_token_balance_1 = self.basic_token.balances["bob"]
        # self.assertAlmostEqual(bob_token_balance, 288000)

        # bob deposit = 10 + 10 + 10
        bob_token_balance_2 = self.basic_token.balances["bob"]
        with self.assertRaises(AssertionError):
            self.contract.withdrawYield(environment=env_2, signer="bob", amount=100000)

    def test_27_insufficient_vtoken_will_fail(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=5, day=1, hour=0)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        bob_token_balance = self.contract.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 10)

        self.contract.transfer(environment=env_1, signer="bob", to="lucy", amount=10)

        bob_token_balance = self.contract.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 0)

        lucy_token_balance = self.contract.balances["lucy"]
        self.assertAlmostEqual(lucy_token_balance, 10)

        with self.assertRaises(AssertionError):
            self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

    def test_28_enough_vtoken_will_pass(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=5, day=1, hour=0)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        bob_token_balance = self.contract.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 10)

        self.contract.transfer(environment=env_1, signer="bob", to="lucy", amount=10)

        bob_token_balance = self.contract.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 0)

        lucy_token_balance = self.contract.balances["lucy"]

        self.assertAlmostEqual(lucy_token_balance, 10)
        self.contract.transfer(environment=env_2, signer="lucy", to="bob", amount=10)

        # bob deposit = 10 + 10 + 10
        self.contract.withdrawTokensAndYield(environment=env_2, signer="bob")

    def test_29_xfer_from_vtoken_should_pass(self):

        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_2 = {"now": Datetime(year=2021, month=5, day=1, hour=0)}

        self.contract.setDevRewardPct(amount=0)
        self.contract.changeAmountPerHour(amount_per_hour=10)

        self.contract.addStakingTokens(environment=env_1, signer="bob", amount=10)

        bob_token_balance = self.contract.balances["bob"]
        self.assertAlmostEqual(bob_token_balance, 10)

        self.contract.transfer_from(
            environment=env_2,
            signer="con_staking_smart_epoch",
            amount=10,
            to="con_staking_smart_epoch",
            main_account="bob",
        )

        contract_token_balance = self.contract.balances["con_staking_smart_epoch"]

        self.assertAlmostEqual(contract_token_balance, 10)

    def setUpDex(self):
        self.currency.approve(amount=10000000000, to="dex")
        self.rswp.approve(amount=10000000000, to="dex")
        self.dex.create_market(
            contract="con_rswp", currency_amount=100, token_amount=100
        )
        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        self.dex.add_liquidity(contract="con_rswp", currency_amount=100000)
        # self.dex.approve_liquidity(contract="con_rswp", to="sys", amount=5000)
        self.currency.approve(signer="bob", amount=999999999999, to="dex")
        self.currency.approve(signer="bob", amount=999999999999, to="dex")
        self.currency.approve(signer="sys", amount=999999999999, to="bob")
        self.rswp.approve(signer="bob", amount=999999999999, to="dex")
        self.rswp.transfer(to="bob", amount=1000)
        self.dex.approve_liquidity(
            signer="bob",
            contract="con_rswp",
            to="con_liquidity_mining_smart_epoch",
            amount=10000,
        )
        self.contract_single_asset.addToTrustedExporters(contract="con_liquidity_mining_smart_epoch")
        self.yield_farm.addToTrustedImporters(
            contract="con_staking_smart_epoch_single_asset"
        )
        self.yield_farm.setDevRewardPct(amount=0)
        self.basic_token.transfer(
            to="con_staking_smart_epoch_single_asset", amount=100000
        )
        self.basic_token.transfer(to="con_liquidity_mining_smart_epoch", amount=100000)

    def test_30_stakeFromContractProfits_liquidity_mining_one_deposit_passes(self):
        self.setUpDex()

        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}

        # bob stakes LP
        self.dex.add_liquidity(signer="bob", contract="con_rswp", currency_amount=1000)

        self.yield_farm.addStakingTokens(environment=env_0, signer="bob", amount=1000)

        # after 1 hour, withdraws rewards to staking contract
        self.contract_single_asset.stakeFromContractProfits(
            environment=env_1, signer="bob", contract="con_liquidity_mining_smart_epoch"
        )
        # check that staking contract has received his deposit.
        bob_deposit = self.contract_single_asset.Deposits["bob"]
        self.assertAlmostEquals(bob_deposit["amount"], 3000)

    def test_31_stakeFromContractProfits_liquidity_mining_two_deposits_passes(self):
        self.setUpDex()
        self.contract_single_asset.changeAmountPerHour(amount_per_hour=0)

        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        # bob stakes LP
        self.dex.add_liquidity(signer="bob", contract="con_rswp", currency_amount=1000)

        # Puts LP in Yield Farming Contract
        bob_lp_balance = self.dex.lp_points["con_rswp", "bob"]

        self.yield_farm.addStakingTokens(environment=env_0, signer="bob", amount=1000)

        # after 1 hour, withdraws rewards to staking contract
        self.contract_single_asset.stakeFromContractProfits(
            environment=env_1, signer="bob", contract="con_liquidity_mining_smart_epoch"
        )

        self.contract_single_asset.stakeFromContractProfits(
            environment=env_2, signer="bob", contract="con_liquidity_mining_smart_epoch"
        )
        # check that staking contract has received his deposit.
        bob_deposit = self.contract_single_asset.Deposits["bob"]
        self.assertAlmostEquals(bob_deposit["amount"], 6000)

        bob_vtokens = self.contract_single_asset.balances["bob"]
        self.assertAlmostEquals(bob_vtokens, 6000)

    def test_32_stakeFromContractProfits_no_lp_fails(self):
        self.setUpDex()
        self.contract_single_asset.changeAmountPerHour(amount_per_hour=0)

        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        with self.assertRaises(AssertionError):
            self.contract_single_asset.stakeFromContractProfits(
                environment=env_1,
                signer="bob",
                contract="con_liquidity_mining_smart_epoch",
            )


    def test_33_stakeFromContractProfits_not_trusted_importer_fails(self):
        self.setUpDex()
        self.contract_single_asset.changeAmountPerHour(amount_per_hour=0)
        self.yield_farm.removeFromTrustedImporters(
            contract="con_staking_smart_epoch_single_asset"
        )

        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        with self.assertRaises(AssertionError):
            self.contract_single_asset.stakeFromContractProfits(
                environment=env_1,
                signer="bob",
                contract="con_liquidity_mining_smart_epoch",
            )


    def test_34_stakeFromContractProfits_not_trusted_exporter_fails(self):
        self.setUpDex()
        self.contract_single_asset.changeAmountPerHour(amount_per_hour=0)
        self.contract_single_asset.removeFromTrustedExporters(contract="con_liquidity_mining_smart_epoch")

        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}

        with self.assertRaises(AssertionError):
            self.contract_single_asset.stakeFromContractProfits(
                environment=env_1,
                signer="bob",
                contract="con_liquidity_mining_smart_epoch",
            )

    def test_35_stakeFromContractProfits_lp_contract_no_yield_token_balance_fails(self):
        env_0 = {"now": Datetime(year=2021, month=1, day=1, hour=0)}
        env_1 = {"now": Datetime(year=2021, month=1, day=1, hour=1)}
        env_2 = {"now": Datetime(year=2021, month=1, day=1, hour=2)}
        
        self.setUpDex()

        # self.basic_token.approve(amount=999999999999, to="burn")
        self.basic_token.transfer(signer="con_liquidity_mining_smart_epoch", to="burn", amount=100000)

        self.dex.approve_liquidity(
            contract="con_rswp",
            to="con_liquidity_mining_smart_epoch",
            amount=1000,
        )
        self.yield_farm.addStakingTokens(
            environment=env_0,
            amount=1000)

        with self.assertRaises(AssertionError):
            self.contract_single_asset.stakeFromContractProfits(
                environment=env_1,
                contract="con_liquidity_mining_smart_epoch",
            )



if __name__ == "__main__":
    unittest.main()
