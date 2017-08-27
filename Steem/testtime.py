from steem import Steem
from steem.account import Account

account = Account('raffle')
s = Steem()
s.commit.transfer('raffle', 1, 'SBD', 'hi', 'steemitraffle')
#s.commit.transfer('steemitraffle', 1, 'SBD', 'hi', 'raffle')
#print(next(account.get_account_history(1000, 1000)))
