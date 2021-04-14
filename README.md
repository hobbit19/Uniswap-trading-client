# Uniswap trading client

![alt text](https://github.com/aviddot/Uniswap-trading-client/raw/main/testv03.gif "GIF application")

<H2>Prerequisites</H2>

- An ethereum address
- An infura project with link (www.infura.io)
- A Windows machine
- <i>Not sure whether needed anymore: Visual C++ build tools (www.visualstudio.microsoft.com/visual-cpp-build-tools/)</i>

<br> </br>
<H2>Getting started</H2>

0. Read prerequisites

1. Download the latest release or download "configfile.py" and "bot.exe" from the repository.


2. Open "configfile.py" (with notepad for instance) and add your ethereum address and personal key at the bottom of the file between the quotation marks('').

<pre>...
my_address = ''
my_pk = ''</pre>


3. Run "bot.exe"

- Make sure configfile.py and bot.exe are in the same folder.


5. Edit settings according to choice.

6. Add infura project url

<br> </br>
<H2>Functions</H2>


<b>Main coin/token</b>: The token or coin you want to trade tokens for and with

<b>Buy/Sell boundary</b>: The amount of balance (calculated in $) that a token or your main coin/token has to be present to deduct whether the latest action was a buy or a sell. For instance: in the value is 100 ,your maincoin option ethereum and have 120$ worth of ethereum on your address, the bot will see the latest action as "sell".

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

<b>Max GWEI</b>: Set a limit to how much GWEI you want to use. If the chosen gas strategie gives a higher GWEI than the limit, the transaction wont be made.

<b>Different deposit address</b>: Use this if you want the swap output to go to a different ethereum address (without extra fees).

<b>Tokentokennumerator (Experimental!)</b>: This value lets you trade ERC tokens with each other. The code to create the value is as followed:

<pre>if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken2usd < ((token2high + token2low) / 2):
  token1totoken2 = ((pricetoken1usd - token1low) / (token1high - token1low)) / ((pricetoken2usd - token2low) / (token2high - token2low))</pre>
  
  If you dont want to wait till the token1 is sold for the maincoinoption, because you are uncertain whether token2 will still be at this price level or think that token1 will     drop, you can use this function. To use this function, "Trade with ERC" should be activated for at least 2 tokens, and the highs and lows should be set seriously.
    
  As an example, if the current price of token1 is $0.9 and its set "high"=$1 and "low"=$0, the value of this token is seen as "90%". Token2 also has a high of $1, but the         current price is 0.2$, value of this token is seen as 20%. The tokentokenmnumerator is set at 3.3. If we divide the 90% by the 20%, we get 4.5, which is higher than 3.3, which   means that token1 gets traded for token2 instantly. If the tokentokennumerator was set to 5, the swap would not happen.
  
<br> </br>
<H2>Changelog v1</h2>

- Several bug fixes that were found after testing all feature
- Added current balances in $. The bot now tells you how much balance your account has.
- Added buy-sell boundary. This value tells the bot how much ETH (or token such as USDT) is needed to be on the address to see the last action as a sell.
- ...
- Repacked into an executable due to edited modules and questions about python usage
- Fixed problems regarding threading, the trader works much faster now
- Further updates in custom gas strategies
- Added the option to apply the maximum amount of GWEI you want to use
- Added the option to send the swap output straight to a different address, without extra fees

<br> </br>
<H2>Current bugs</h2>


- Using wBTC or eth as token is not possible, but it is possible to use them as main-coin/token
- Sloppy dinamic design of GUI
- Sometimes lag when updating names or when starting the bot (0-10 seconds)
- More: Let me know!

<br> </br>
<H2>To do</H2>

- New, more user-friendly design

(Depends on whether the application is used)

<br> </br>
<H2>Author</H2>
During the latest pandemic I realised that I had time to learn how to code, I decided to do this by making trader-bots in python. Other than it being a good exercise, it was/is also very fun and lucrative! This is one of my first applications I made, so the documentation is still quite poor with spaghetti-code here and there, but it does what it should do!



<br> </br>
<H2>Disclosure</H2>
I own some of the tokens portayed in the gif. These tokens are used only for example purposes and are not meant to be an endorsement. I am not affiliated with these tokens or any subsidiaries. Use the application at your own risk, I am not in any way responsible for losses.

  
