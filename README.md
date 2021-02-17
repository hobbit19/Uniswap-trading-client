# Uniswap-trader-GUI
A Uniswap V2 trader client with GUI, limit orders and stoploss.

<H2>Prerequisites</H2>

- An ethereum address and its personal key
- An infura project with link

<H2>Getting started</H2>

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


<H2>Functions</H2>


<b>Main coin/token</b>: The token or coin you want to trade tokens for and with

<b>Token ETH address</b>: Fill the token eth address you want to trade (such as 0x00000000000000000)

<b>Low($)</b>: The price you want the trader to sell the token for (0.01 = 1 dollar cent)

<b>High($)</b>: The price you want the trader to buy the token for (0.01 = 1 dollar cent)

<b>Activate and Trade with ETH</b>: Toggle if you want to activate trading with your main coin/token

<b>Trade with ERC (Experimental!)</b>: Toggle if you want to trade the token with other ERC tokens of which this option is activated (see tokentokennumerator)

<b>Stoploss</b>: Toggle to activate stoploss (0.01 = 1 dollar cent)


<b>Second(s) between checking price</b>: Standard is 4 seconds. With a infura server with max 100.000tx/day 4 seconds is good for 2 activated token 24hr/day


<b>Seconds waiting between trades</b>: depends on how fast transactions finalize
<b>Max slippage</b>: The maximum slippage you want to allow while trading (0.03 = 3%)
<b>$ to keep in ETH after trade</b>: The amount of ETH/main token you want to keep after each trade (excluding transaction fee's) in terms of $.
<b>GWEI option</b>: The amount of gas you want to use for each trade (see ethgasstation.info) <b>Under construction: use fast</b>
<b>Update names</b>: Press to update tokens names according to the Token address


<b>Tokentokennumerator (Experimental!)</b>: This value lets you trade ERC tokens with each other. The code to create the value is as follows:

<pre>if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken2usd < ((token2high + token2low) / 2):
  token1totoken2 = ((pricetoken1usd - token1low) / (token1high - token1low)) / ((pricetoken2usd - token2low) / (token2high - token2low))</pre>
  
  If you dont want to wait till the token1 is sold for the maincoinoption, because you are uncertain whether token2 will still be at this price level or think that token1 will     drop, you can use this function. To use this function, "Trade with ERC" should be activated for at least 2 tokens, and the highs and lows set seriously.
    
  As an example, if the current price of token1 is $0.9 and it's set high is $1, the value of this token is "seen as 90%". Token2 also has a high of $1, but the current price is   0.2$, value of this token is seen as 20%. The tokentokenmnumerator is set at 3.3. If we divide the 90% by the 20%, we get 4.5, which is higher than 3.3, which means that         token1 gets traded for token2 instantly. If the tokentokennumerator was set to 5, the swap would not happen.

<H2>Current bugs</h2>

- Cant add current ETH tokens with less than 18 decimals (The price it shows will be wrong)
- Starting the bot after it is been stopped may close the application in Linux (No problem in Windows)
- Sloppy dinamic design of GUI
- More: Let me know!


<H2>To do</H2>

- Fix bugs
- New, more user-friendly design
(Depends on whether the application is used)
  
