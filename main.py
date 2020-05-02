from runner import Runner
from store import Store

store = Store()

runner = Runner(store)
runner.run()
