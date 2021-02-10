# Uniswap-trader-GUI
A Uniswap V2 trader client with GUI, limit orders and stoploss.

<H3>Prerequisites</H3>

- An ethereum address and its personal key
- An infura project with link

<H3>Getting started</H3>

1. Download the files from this git-repository.

2. Install the modules needed for the trader using pip.

<pre>pip install -r requirements.txt</pre>

3. Open "configfile.py" and add your ethereum address and personal key at the bottom of the file between the quotation marks('').

<pre>...
my_address = ''
my_pk = ''</pre>


4. Run "bot.py"

<pre>python bot.py</pre>

5. Edit settings according to choice.

6. Add infura project url


<H3>Functions</H3>
<b>Main coin/token</b>: The token or coin you want to trade tokens for and with

<b>Token ETH address</b>: Fill the token eth address you want to trade (such as 0x00000000000000000)

<b>Low($)</b>: The price you want the trader to sell the token for (0.01 = 1 dollar cent)

<b>High($)</b>: The price you want the trader to buy the token for (0.01 = 1 dollar cent)

<b>Activate and Trade with ETH</b>: Toggle if you want to activate trading with your main coin/token

<b>Trade with ERC (Experimental!)</b>: Toggle if you want to trade the token with other ERC tokens of which this option is activated

<b>Stoploss</b>: Toggle to activate stoploss (0.01 = 1 dollar cent)


<b>Second(s) between checking price</b>: Standard is 4 seconds. With a infura server with max 100.000tx/day 4 seconds is good for 2 activated token 24hr/day

<b>Tokentokennumerator (Experimental!)</b>: ...

<b>Seconds waiting between trades</b>: depends on how fast transactions finalize
<b>Max slippage</b>: The maximum slippage you want to allow while trading (0.03 = 3%)
<b>$ to keep in ETH after trade</b>: Ther amount of ETH/main token you want to keep after each trade (excluding transaction fee's) in terms of $.
<b>GWEI option</b>: The amount of gas you want to use for each trade (see ethgasstation.info)
