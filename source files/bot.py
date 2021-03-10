import datetime
import time
from uniswap import Uniswap
from web3 import Web3, middleware, _utils
from web3.gas_strategies.time_based import fast_gas_price_strategy,fastfast_gas_price_strategy,mediummedium_gas_price_strategy,glacial_gas_price_strategy
from pycoingecko import CoinGeckoAPI
import pyetherbalance
import requests
import math
import subprocess
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget,QGraphicsObject
from PyQt5.QtCore import QCoreApplication
import fileinput
import re
import importlib
import os
from time import localtime, strftime
from web3 import types
import traceback
sys.path.insert(0, './')
import configfile



QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons


def __ne__(self, other):
    return not self.__eq__(other)


cg = CoinGeckoAPI()


class Port(object):
    def __init__(self, view):
        self.view = view

    def flush(self):
        pass

    def write(self, text):
        cursor = self.view.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.view.setTextCursor(cursor)
        self.view.ensureCursorVisible()


@pyqtSlot(str)
def trap_exc_during_debug(*args):
    if configfile.debugmode == '1':
        exception_type, exception_object, exception_traceback = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


sys.excepthook = trap_exc_during_debug


@pyqtSlot()
class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """
    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False

    def work(self):
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
        self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))


        if 'step' not in globals():
            step=1
        else:
            step=step+1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()
        if self.__abort==True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

        importlib.reload(configfile)
        w33 = Web3()
        cg = CoinGeckoAPI()
        maxgwei=float(configfile.maxgwei)
        maxgweinumber = int(configfile.maxgweinumber)
        diffdeposit=float(configfile.diffdeposit)
        diffdepositaddress = str(configfile.diffdepositaddress)
        speed = str(configfile.speed)
        max_slippage = float(configfile.max_slippage)
        incaseofbuyinghowmuch = int(configfile.incaseofbuyinghowmuch)
        ethtokeep = int(configfile.ethtokeep)
        timesleepaftertrade = int(configfile.secondscheckingprice_2)
        timesleep = int(configfile.secondscheckingprice)
        infura_url = str(configfile.infuraurl)
        infuraurl = infura_url
        tokentokennumerator = float(configfile.tokentokennumerator)
        activatetoken1 = float(configfile.activatetoken1)
        tradewithETHtoken1 = float(configfile.tradewithETHtoken1)
        tradewithERCtoken1 = float(configfile.tradewithERCtoken1)
        token1ethaddress = str(configfile.token1ethaddress)
        token1low = float(configfile.token1low)
        token1high = float(configfile.token1high)
        token1ethaddress = str(configfile.token1ethaddress)
        token1low = float(configfile.token1low)
        token1high = float(configfile.token1high)
        activatetoken2 = float(configfile.activatetoken2)
        tradewithETHtoken2 = float(configfile.tradewithETHtoken2)
        tradewithERCtoken2 = float(configfile.tradewithERCtoken2)
        token2ethaddress = str(configfile.token2ethaddress)
        token2low = float(configfile.token2low)
        token2high = float(configfile.token2high)
        token2ethaddress = str(configfile.token2ethaddress)
        token2low = float(configfile.token2low)
        token2high = float(configfile.token2high)
        activatetoken3 = float(configfile.activatetoken3)
        tradewithETHtoken3 = float(configfile.tradewithETHtoken3)
        tradewithERCtoken3 = float(configfile.tradewithERCtoken3)
        token3ethaddress = str(configfile.token3ethaddress)
        token3low = float(configfile.token3low)
        token3high = float(configfile.token3high)
        token3ethaddress = str(configfile.token3ethaddress)
        token3low = float(configfile.token3low)
        token3high = float(configfile.token3high)
        activatetoken4 = float(configfile.activatetoken4)
        tradewithETHtoken4 = float(configfile.tradewithETHtoken4)
        tradewithERCtoken4 = float(configfile.tradewithERCtoken4)
        token4ethaddress = str(configfile.token4ethaddress)
        token4low = float(configfile.token4low)
        token4high = float(configfile.token4high)
        token4ethaddress = str(configfile.token4ethaddress)
        token4low = float(configfile.token4low)
        token4high = float(configfile.token4high)
        activatetoken5 = float(configfile.activatetoken5)
        tradewithETHtoken5 = float(configfile.tradewithETHtoken5)
        tradewithERCtoken5 = float(configfile.tradewithERCtoken5)
        token5ethaddress = str(configfile.token5ethaddress)
        token5low = float(configfile.token5low)
        token5high = float(configfile.token5high)
        token5ethaddress = str(configfile.token5ethaddress)
        token5low = float(configfile.token5low)
        token5high = float(configfile.token5high)
        activatetoken6 = float(configfile.activatetoken6)
        tradewithETHtoken6 = float(configfile.tradewithETHtoken6)
        tradewithERCtoken6 = float(configfile.tradewithERCtoken6)
        token6ethaddress = str(configfile.token6ethaddress)
        token6low = float(configfile.token6low)
        token6high = float(configfile.token6high)
        token6ethaddress = str(configfile.token6ethaddress)
        token6low = float(configfile.token6low)
        token6high = float(configfile.token6high)
        activatetoken7 = float(configfile.activatetoken7)
        tradewithETHtoken7 = float(configfile.tradewithETHtoken7)
        tradewithERCtoken7 = float(configfile.tradewithERCtoken7)
        token7ethaddress = str(configfile.token7ethaddress)
        token7low = float(configfile.token7low)
        token7high = float(configfile.token7high)
        token7ethaddress = str(configfile.token7ethaddress)
        token7low = float(configfile.token7low)
        token7high = float(configfile.token7high)
        activatetoken8 = float(configfile.activatetoken8)
        tradewithETHtoken8 = float(configfile.tradewithETHtoken8)
        tradewithERCtoken8 = float(configfile.tradewithERCtoken8)
        token8ethaddress = str(configfile.token8ethaddress)
        token8low = float(configfile.token8low)
        token8high = float(configfile.token8high)
        token8ethaddress = str(configfile.token8ethaddress)
        token8low = float(configfile.token8low)
        token8high = float(configfile.token8high)
        activatetoken9 = float(configfile.activatetoken9)
        tradewithETHtoken9 = float(configfile.tradewithETHtoken9)
        tradewithERCtoken9 = float(configfile.tradewithERCtoken9)
        token9ethaddress = str(configfile.token9ethaddress)
        token9low = float(configfile.token9low)
        token9high = float(configfile.token9high)
        token9ethaddress = str(configfile.token9ethaddress)
        token9low = float(configfile.token9low)
        token9high = float(configfile.token9high)
        activatetoken10 = float(configfile.activatetoken10)
        tradewithETHtoken10 = float(configfile.tradewithETHtoken10)
        tradewithERCtoken10 = float(configfile.tradewithERCtoken10)
        token10ethaddress = str(configfile.token10ethaddress)
        token10low = float(configfile.token10low)
        token10high = float(configfile.token10high)
        token10ethaddress = str(configfile.token10ethaddress)
        token10low = float(configfile.token10low)
        token10high = float(configfile.token10high)

        stoplosstoken10 = float(configfile.token10stoploss)
        stoplosstoken9 = float(configfile.token9stoploss)
        stoplosstoken8 = float(configfile.token8stoploss)
        stoplosstoken7 = float(configfile.token7stoploss)
        stoplosstoken6 = float(configfile.token6stoploss)
        stoplosstoken5 = float(configfile.token5stoploss)
        stoplosstoken4 = float(configfile.token4stoploss)
        stoplosstoken3 = float(configfile.token3stoploss)
        stoplosstoken2 = float(configfile.token2stoploss)
        stoplosstoken1 = float(configfile.token10stoploss)

        stoplosschecktoken1 = float(configfile.stoplosstoken1)
        stoplosschecktoken2 = float(configfile.stoplosstoken2)
        stoplosschecktoken3 = float(configfile.stoplosstoken3)
        stoplosschecktoken4 = float(configfile.stoplosstoken4)
        stoplosschecktoken5 = float(configfile.stoplosstoken5)
        stoplosschecktoken6 = float(configfile.stoplosstoken6)
        stoplosschecktoken7 = float(configfile.stoplosstoken7)
        stoplosschecktoken8 = float(configfile.stoplosstoken8)
        stoplosschecktoken9 = float(configfile.stoplosstoken9)
        stoplosschecktoken10 = float(configfile.stoplosstoken10)
        debugmode = int(configfile.debugmode)

        token1address = token1ethaddress
        token2address = token2ethaddress
        token3address = token3ethaddress
        token4address = token4ethaddress
        token5address = token5ethaddress
        token6address = token6ethaddress
        token7address = token7ethaddress
        token8address = token8ethaddress
        token9address = token9ethaddress
        token10address = token10ethaddress
        fasttoken1 = 0
        fasttoken2 = 0
        fasttoken3 = 0
        fasttoken4 = 0
        fasttoken5 = 0
        fasttoken6 = 0
        fasttoken7 = 0
        fasttoken8 = 0
        fasttoken9 = 0
        fasttoken10 = 0

        if float(token1high) < float(token1low) or float(token2high) < float(token2low) or float(token3high) < float(token3low) or float(token4high) < float(token4low) or float(token5high) < float(token5low) or float(token6high) < float(token6low) or float(token7high) < float(token7low) or float(token8high) < float(token8low) or float(token9high) < float(token9low) or float(token10high) < float(token10low) or float(stoplosstoken1) > float(token1high) or float(stoplosstoken2) > float(token2high) or float(stoplosstoken3) > float(token3high) or float(stoplosstoken4) > float(token4high) or float(stoplosstoken5) > float(token5high) or float(stoplosstoken6) > float(token6high) or float(stoplosstoken7) > float(token7high) or float(stoplosstoken8) > float(token8high) or float(stoplosstoken9) > float(token9high) or float(stoplosstoken10) > float(token10high):
            print(
                'Stopping the script, a tokenlow is higher than its tokenhigh or a stoploss it higher than the tokenhigh')
            time.sleep(42949)
        my_address = str(configfile.my_address)
        my_pk = str(configfile.my_pk)
        pk = my_pk
        if configfile.maincoinoption == 'Ethereum':
            ethaddress = "0x0000000000000000000000000000000000000000"
        if configfile.maincoinoption == 'DAI':
            ethaddress = "0x6b175474e89094c44da98b954eedeac495271d0f"
        if configfile.maincoinoption == 'USDT':
            ethaddress = "0xdac17f958d2ee523a2206206994597c13d831ec7"
        if configfile.maincoinoption == 'USDC':
            ethaddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
        if configfile.maincoinoption == 'wBTC':
            ethaddress = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
        maincoinoption = ethaddress
        append = QtCore.pyqtSignal(str)

        if 'step' not in globals():
            step=1
        else:
            step=step+1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()
        if self.__abort==True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))


        try:
            token1smallcasename = 0
            token2smallcasename = 0
            token3smallcasename = 0
            token4smallcasename = 0
            token5smallcasename = 0
            token6smallcasename = 0
            token7smallcasename = 0
            token8smallcasename = 0
            token9smallcasename = 0
            token10smallcasename = 0
            token1smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token1address, id='ethereum')['symbol']
            token2smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token2address, id='ethereum')['symbol']
            token3smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token3address, id='ethereum')['symbol']
            token4smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token4address, id='ethereum')['symbol']
            token5smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token5address, id='ethereum')['symbol']
            token6smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token6address, id='ethereum')['symbol']
            token7smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token7address, id='ethereum')['symbol']
            token8smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token8address, id='ethereum')[
                    'symbol']
            token9smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token9address, id='ethereum')[
                    'symbol']
            token10smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=token10address, id='ethereum')[
                    'symbol']
        except Exception as e:
            o = 0

        def apidecimals(ethaddress):
            res = requests.get(
                'https://api.ethplorer.io/getTokenInfo/' + ethaddress + '?apiKey=EK-5nuDS-iZCPJhW-SYGLU')
            data = int((res.json())["decimals"])
            return data

        try:
            token1decimals = 0
            token2decimals = 0
            token3decimals = 0
            token4decimals = 0
            token5decimals = 0
            token6decimals = 0
            token7decimals = 0
            token8decimals = 0
            token9decimals = 0
            token10decimals = 0
            maindecimals = apidecimals(ethaddress)
            token1decimals = apidecimals(token1address)
            token2decimals = apidecimals(token2address)
            token3decimals = apidecimals(token3address)
            token4decimals = apidecimals(token4address)
            token5decimals = apidecimals(token5address)
            token6decimals = apidecimals(token6address)
            token7decimals = apidecimals(token7address)
            token8decimals = apidecimals(token8address)
            token9decimals = apidecimals(token9address)
            token10decimals = apidecimals(token10address)

        except:
            o = 0

        if 'step' not in globals():
            step=1
        else:
            step=step+1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()
        if self.__abort==True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))

        def letstrade(keer2, tradewithERCtoken1, tradewithERCtoken2, tradewithERCtoken3, tradewithERCtoken4,
                      tradewithERCtoken5, tradewithERCtoken6, tradewithERCtoken9, tradewithERCtoken7,
                      tradewithERCtoken8, tradewithERCtoken10, activatetoken1, activatetoken2, activatetoken3,
                      activatetoken4, activatetoken5, activatetoken6, activatetoken9, activatetoken7,
                      activatetoken8, activatetoken10, tradewithETHtoken1, tradewithETHtoken2, tradewithETHtoken3,
                      tradewithETHtoken4, tradewithETHtoken5, tradewithETHtoken6, tradewithETHtoken9,
                      tradewithETHtoken7, tradewithETHtoken8, tradewithETHtoken10, my_address, pk, max_slippage,
                      infura_url, gelukt,
                      tokentokennumerator,
                      weergave, notyet, priceeth, pricetoken1usd, pricetoken2usd, token1totoken2, token2totoken1,
                      pricetoken3usd, pricetoken4usd, pricetoken5usd,
                      pricetoken6usd, pricetoken7usd, pricetoken8usd, pricetoken9usd, pricetoken10usd,
                      token1totoken7, token1totoken8, token1totoken9,
                      token1totoken3, token1totoken4, token1totoken5, token1totoken6, token1totoken10,
                      token2totoken3, token2totoken4, token2totoken5,
                      token2totoken6, token2totoken7, token2totoken8, token2totoken9, token2totoken10,
                      token3totoken1, token3totoken2, token3totoken4,
                      token3totoken5, token3totoken6, token3totoken7, token3totoken8, token3totoken9,
                      token3totoken10, token4totoken1, token4totoken2,
                      token4totoken3, token4totoken5, token4totoken6, token4totoken7, token4totoken8,
                      token4totoken9, token4totoken10, token5totoken1,
                      token5totoken2, token5totoken4, token5totoken3, token5totoken6, token5totoken7,
                      token5totoken8, token5totoken9, token5totoken10,
                      token6totoken1, token6totoken2, token6totoken4, token6totoken5, token6totoken3,
                      token6totoken7, token6totoken8, token6totoken9,
                      token6totoken10, token7totoken1, token7totoken2, token7totoken4, token7totoken5,
                      token7totoken6, token7totoken3, token7totoken8,
                      token7totoken9, token7totoken10, token8totoken1, token8totoken2, token8totoken4,
                      token8totoken5, token8totoken6, token8totoken7,
                      token8totoken3, token8totoken9, token8totoken10, token9totoken1, token9totoken2,
                      token9totoken4, token9totoken5, token9totoken6,
                      token9totoken7, token9totoken8, token9totoken3, token9totoken10, token10totoken1,
                      token10totoken2, token10totoken4, token10totoken5,
                      token10totoken6, token10totoken7, token10totoken8, token10totoken9, token10totoken3,
                      token1address, token1smallcasename, token2address, token2smallcasename, token3address,
                      token3smallcasename,
                      token4address, token4smallcasename, token5address, token5smallcasename, token6address,
                      token6smallcasename,
                      token7address, token7smallcasename, token8address, token8smallcasename, token9address,
                      token9smallcasename,
                      token10address, token10smallcasename, token1high, token1low, token2high, token2low,
                      token3high,
                      token3low,
                      token4high, token4low, token5high, token5low, token6high, token6low, token7high, token7low,
                      token8high,
                      token8low, token9high, token9low, token10high, token10low, incaseofbuyinghowmuch,
                      timesleepaftertrade,
                      ethtokeep, maincoinoption, fasttoken1, fasttoken2, fasttoken3, fasttoken4, fasttoken5, fasttoken6,
                      fasttoken7, fasttoken8, fasttoken9, fasttoken10, stoplosstoken1, stoplosstoken2, stoplosstoken3,
                      stoplosstoken4, stoplosstoken5, stoplosstoken6, stoplosstoken7, stoplosstoken8, stoplosstoken9,
                      stoplosstoken10, stoplosschecktoken1, stoplosschecktoken2, stoplosschecktoken3,
                      stoplosschecktoken4, stoplosschecktoken5, stoplosschecktoken6, stoplosschecktoken7,
                      stoplosschecktoken8, stoplosschecktoken9, stoplosschecktoken10,
                      token1decimals, token2decimals, token3decimals, token4decimals, token5decimals, token6decimals,
                      token7decimals, token8decimals, token9decimals, token10decimals, speed,maxgwei,maxgweinumber,diffdeposit,diffdepositaddress):

            def makeTrade(buytokenaddress, selltokenaddress, my_address, pk, max_slippage, infura_url,
                          buysmallcasesymbol, sellsmallcasesymbol, ethtokeep, speed,maxgwei,maxgweinumber,diffdeposit,diffdepositaddress,ethaddress):
                def api2(ethaddress):
                    res = requests.get(
                        'https://api.ethplorer.io/getTokenInfo/' + ethaddress + '?apiKey=EK-5nuDS-iZCPJhW-SYGLU')
                    data = int((res.json())["decimals"])
                    return data

                selldecimals = int(api2(selltokenaddress))
                try:
                    def api(speed):
                        res = requests.get(
                            'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                        data = (res.json()[speed]) / 10
                        return data

                    gwei = api(speed)
                    print('Gwei for ' + str(speed) + ' trading at the moment: ' + str(gwei))
                    gwei=types.Wei(Web3.toWei(gwei, "gwei"))

                except Exception as e:
                    o = 0
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                if (maxgwei==0) or (maxgwei==1 and gwei <= maxgweinumber):

                    try:
                        uniconnect = Uniswap(my_address, pk, web3=Web3(
                            w33.HTTPProvider(infura_url)),
                                             version=2, max_slippage=max_slippage)
                        eth = Web3.toChecksumAddress(selltokenaddress)
                        token = w33.toChecksumAddress(buytokenaddress)
                        selldecimals = int(api2(selltokenaddress))
                    except Exception as e:
                        print(e)
                    try:
                        if sellsmallcasesymbol == "eth":
                            ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                            balance_eth = ethbalance.get_eth_balance(my_address)
                            priceeth = cg.get_price(ids='ethereum', vs_currencies='usd')
                            ethamount2 = (float(balance_eth['balance'])) - (
                                    ethtokeep / (float(priceeth['ethereum']['usd'])))
                        else:
                            ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                            balance_eth = ethbalance.get_eth_balance(my_address)
                            token2 = sellsmallcasesymbol.upper
                            details2 = {'symbol': sellsmallcasesymbol.upper, 'address': selltokenaddress,
                                        'decimals': selldecimals,
                                        'name': sellsmallcasesymbol.upper}
                            erc20tokens2 = ethbalance.add_token(token2, details2)
                            ethamount2 = math.floor(
                                ethbalance.get_token_balance(token2, ethereum_address)['balance'])
                        tradeamount = ethamount2 * 10 ** selldecimals
                        ethamount = tradeamount
                        eth = Web3.toChecksumAddress(selltokenaddress)
                        token = w33.toChecksumAddress(buytokenaddress)
                        contractaddress = token
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    tradeamount = (ethamount2 * 10 ** selldecimals)
                    ethamount = ethamount2
                    contractaddress = token
                    if int(diffdeposit) == 0:
                        uniconnect.make_trade(eth, token, int(tradeamount),gwei,my_address,pk)
                    if int(diffdeposit) == 1:
                        uniconnect.make_trade(eth, token, int(tradeamount), gwei, my_address, pk,diffdepositaddress)

                    if buytokenaddress == ethaddress:
                        gelukt = 'sell'
                    if buytokenaddress != ethaddress:
                        gelukt = 'buy ' + buysmallcasesymbol
                    return {'gelukt': gelukt}
                else:
                    print('Current gwei  of gasstrategy are higher than max-gwei')
                    gelukt='mislukt'
                    return {'gelukt': gelukt}

            try:  # self added
                o = 0
            except:
                o = 0
            try:  # stop loss
                if (
                        pricetoken1usd < stoplosstoken1 and stoplosschecktoken1 == 1 and activatetoken1 == 1 and tradewithETHtoken1 == 1 and gelukt == "buy " + token1smallcasename) or (
                        pricetoken1usd < stoplosstoken1 and activatetoken1 == 1 and tradewithETHtoken1 == 1 and gelukt2 == "buy " + token1smallcasename and stoplosschecktoken1 == 1):
                    print("Selling " + str(
                        token1smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken1usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token1address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken1 = 0
                if (
                        pricetoken2usd < stoplosstoken2 and activatetoken2 == 1 and stoplosschecktoken2 == 1 and tradewithETHtoken2 == 1 and gelukt == "buy " + token2smallcasename) or (
                        pricetoken2usd < stoplosstoken2 and activatetoken2 == 1 and tradewithETHtoken2 == 1 and gelukt2 == "buy " + token2smallcasename and stoplosschecktoken2 == 1):
                    print("Selling " + str(
                        token2smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken2usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token2address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken2 = 0
                if (
                        pricetoken3usd < stoplosstoken3 and activatetoken3 == 1 and stoplosschecktoken3 == 1 and tradewithETHtoken3 == 1 and gelukt == "buy " + token3smallcasename) or (
                        pricetoken3usd < stoplosstoken3 and activatetoken3 == 1 and tradewithETHtoken3 == 1 and gelukt2 == "buy " + token3smallcasename and stoplosschecktoken3 == 1):
                    print("Selling " + str(
                        token3smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken3usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token3address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken3 = 0
                if (
                        pricetoken4usd < stoplosstoken4 and activatetoken4 == 1 and stoplosschecktoken4 == 1 and tradewithETHtoken4 == 1 and gelukt == "buy " + token4smallcasename) or (
                        pricetoken4usd < stoplosstoken4 and activatetoken4 == 1 and tradewithETHtoken4 == 1 and gelukt2 == "buy " + token4smallcasename and stoplosschecktoken4 == 1):
                    print("Selling " + str(
                        token4smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken4usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token4address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken4 = 0
                if (
                        pricetoken5usd < stoplosstoken5 and activatetoken5 == 1 and stoplosschecktoken5 == 1 and tradewithETHtoken5 == 1 and gelukt == "buy " + token5smallcasename) or (
                        pricetoken5usd < stoplosstoken5 and activatetoken5 == 1 and tradewithETHtoken5 == 1 and gelukt2 == "buy " + token5smallcasename and stoplosschecktoken5 == 1):
                    print("Selling " + str(
                        token5smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken5usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token5address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken5 = 0
                if (
                        pricetoken6usd < stoplosstoken6 and activatetoken6 == 1 and stoplosschecktoken6 == 1 and tradewithETHtoken6 == 1 and gelukt == "buy " + token6smallcasename) or (
                        pricetoken6usd < stoplosstoken6 and activatetoken6 == 1 and tradewithETHtoken6 == 1 and gelukt2 == "buy " + token6smallcasename and stoplosschecktoken6 == 1):
                    print("Selling " + str(
                        token6smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken6usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token6address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken6 = 0
                if (
                        pricetoken7usd < stoplosstoken7 and activatetoken7 == 1 and stoplosschecktoken7 == 1 and tradewithETHtoken7 == 1 and gelukt == "buy " + token7smallcasename) or (
                        pricetoken7usd < stoplosstoken7 and activatetoken7 == 1 and tradewithETHtoken7 == 1 and gelukt2 == "buy " + token7smallcasename and stoplosschecktoken7 == 1):
                    print("Selling " + str(
                        token7smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken7usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token7address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken7 = 0
                if (
                        pricetoken8usd < stoplosstoken8 and activatetoken8 == 1 and stoplosschecktoken8 == 1 and tradewithETHtoken8 == 1 and gelukt == "buy " + token8smallcasename) or (
                        pricetoken8usd < stoplosstoken8 and activatetoken8 == 1 and tradewithETHtoken8 == 1 and gelukt2 == "buy " + token8smallcasename and stoplosschecktoken8 == 1):
                    print("Selling " + str(
                        token8smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken8usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token8address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken8 = 0
                if (
                        pricetoken9usd < stoplosstoken9 and activatetoken9 == 1 and stoplosschecktoken9 == 1 and tradewithETHtoken9 == 1 and gelukt == "buy " + token9smallcasename) or (
                        pricetoken9usd < stoplosstoken9 and activatetoken9 == 1 and tradewithETHtoken9 == 1 and gelukt2 == "buy " + token9smallcasename and stoplosschecktoken9 == 1):
                    print("Selling " + str(
                        token9smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken9usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token9address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken9 = 0
                if (
                        pricetoken10usd < stoplosstoken10 and activatetoken10 == 1 and stoplosschecktoken10 == 1 and tradewithETHtoken10 == 1 and gelukt == "buy " + token10smallcasename) or (
                        pricetoken10usd < stoplosstoken10 and activatetoken10 == 1 and tradewithETHtoken10 == 1 and gelukt2 == "buy " + token10smallcasename and stoplosschecktoken10 == 1):
                    print("Selling " + str(
                        token10smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                        pricetoken10usd) + ')')
                    if maincoinoption != '0x0000000000000000000000000000000000000000':
                        buysmallcasesymbol = str(
                            cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                         id='ethereum')['symbol'])
                    else:
                        buysmallcasesymbol = 'eth'
                    kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token10address,
                                     my_address=my_address,
                                     pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                     buysmallcasesymbol=buysmallcasesymbol,
                                     sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                    time.sleep(timesleepaftertrade)
                    gelukt = kaka['gelukt']
                    keer = 9999
                    fasttoken10 = 0
            except:
                o = 0
                gelukt = 'mislukt'
            try:  # sell alt and buy ETH trades
                if (token1address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1:
                    if (pricetoken1usd > token1high and gelukt == "buy " + token1smallcasename) or (
                            pricetoken1usd > token1high and gelukt2 == "buy " + token1smallcasename) or (
                            activatetoken1 == 1 and gelukt == 'buy ' + token1smallcasename and fasttoken1 == 1):
                        print("Selling " + str(
                            token1smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken1usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token1address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken1 = 0
                if (token2address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1:
                    if (pricetoken2usd >= token2high and gelukt == "buy " + token2smallcasename) or (
                            pricetoken2usd > token2high and gelukt2 == "buy " + token2smallcasename) or (
                            fasttoken2 == 1):
                        print("Selling " + str(
                            token2smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken2usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token2address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken2 = 0
                if (token3address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1:
                    if (pricetoken3usd > token3high and gelukt == "buy " + token3smallcasename) or (
                            pricetoken3usd > token3high and gelukt2 == "buy " + token3smallcasename) or (
                            fasttoken3 == 1):
                        print("Selling " + str(
                            token3smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken3usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token3address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken3 = 0
                if (token4address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1:
                    if (pricetoken4usd > token4high and gelukt == "buy " + token4smallcasename) or (
                            pricetoken4usd > token4high and gelukt2 == "buy " + token4smallcasename) or (
                            fasttoken4 == 1):
                        print("Selling " + str(
                            token4smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken4usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token4address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken4 = 0
                if (token5address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1:
                    if (pricetoken5usd > token5high and gelukt == "buy " + token5smallcasename) or (
                            pricetoken5usd > token5high and gelukt2 == "buy " + token5smallcasename) or (
                            fasttoken5 == 1):
                        print("Selling " + str(
                            token5smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken5usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token5address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken5 = 0
                if (token6address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1:
                    if (pricetoken6usd > token6high and gelukt == "buy " + token6smallcasename) or (
                            pricetoken6usd > token6high and gelukt2 == "buy " + token6smallcasename) or (
                            fasttoken6 == 1):
                        print("Selling " + str(
                            token6smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken6usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token6address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken6 = 0
                if (token7address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1:
                    if (pricetoken7usd > token7high and gelukt == "buy " + token7smallcasename) or (
                            pricetoken7usd > token7high and gelukt2 == "buy " + token7smallcasename) or (
                            fasttoken7 == 1):
                        print("Selling " + str(
                            token7smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken7usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token7address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken7 = 0
                if (token8address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1:
                    if (pricetoken8usd > token8high and gelukt == "buy " + token8smallcasename) or (
                            pricetoken8usd > token8high and gelukt2 == "buy " + token8smallcasename) or (
                            fasttoken8 == 1):
                        print("Selling " + str(
                            token8smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken8usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token8address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken8 = 0
                if (token9address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1:
                    if (pricetoken9usd > token9high and gelukt == "buy " + token9smallcasename) or (
                            pricetoken9usd > token9high and gelukt2 == "buy " + token9smallcasename) or (
                            fasttoken9 == 1):
                        print("Selling " + str(
                            token9smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken9usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token9address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken9 = 0
                if (token10address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1:
                    if (pricetoken10usd > token10high and gelukt == "buy " + token10smallcasename) or (
                            pricetoken10usd > token10high and gelukt2 == "buy " + token10smallcasename) or (
                            fasttoken10 == 1):
                        print("Selling " + str(
                            token10smallcasename) + ' for Maincoin-option (current price in USD: ' + str(
                            pricetoken10usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            buysmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            buysmallcasesymbol = 'eth'
                        kaka = makeTrade(buytokenaddress=ethaddress, selltokenaddress=token10address,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=buysmallcasesymbol,
                                         sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                        fasttoken10 = 0
            except Exception as e:
                o = 0
                gelukt = "mislukt"
            try:  # sell ETH and buy ALT
                if (token1address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1:
                    if (pricetoken1usd < token1low and gelukt == "sell") or (
                            pricetoken1usd < token1low and gelukt2 == "sell"):
                        print(
                            "Buying " + str(token1smallcasename) + ' (Current price: ' + str(int(pricetoken1usd)) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token1smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token2address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1:
                    if (pricetoken2usd < token2low and gelukt == "sell") or (
                            pricetoken2usd < token2low and gelukt2 == "sell"):
                        print("Buying " + str((token2smallcasename)) + ' (Current price: ' + str(
                            int(pricetoken2usd)) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token2smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token3address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1:
                    if (pricetoken3usd < token3low and gelukt == "sell") or (
                            pricetoken3usd < token3low and gelukt2 == "sell"):
                        print("Buying " + str(token3smallcasename) + ' (Current price: ' + str(pricetoken3usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token3smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token4address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1:
                    if (pricetoken4usd < token4low and gelukt == "sell") or (
                            pricetoken4usd < token4low and gelukt2 == "sell"):
                        print("Buying " + str(token4smallcasename) + ' (Current price: ' + str(pricetoken4usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token4smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token5address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1:
                    if (pricetoken5usd < token5low and gelukt == "sell") or (
                            pricetoken5usd < token5low and gelukt2 == "sell"):
                        print("Buying " + str(token5smallcasename) + ' (Current price: ' + str(pricetoken5usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token5smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token6address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1:
                    if (pricetoken6usd < token6low and gelukt == "sell") or (
                            pricetoken6usd < token6low and gelukt2 == "sell"):
                        print("Buying " + str(token6smallcasename) + ' (Current price: ' + str(pricetoken6usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token6smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token7address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1:
                    if (pricetoken7usd < token7low and gelukt == "sell") or (
                            pricetoken7usd < token7low and gelukt2 == "sell"):
                        print("Buying " + str(token7smallcasename) + ' (Current price: ' + str(pricetoken7usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token7smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token8address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1:
                    if (pricetoken8usd < token8low and gelukt == "sell") or (
                            pricetoken8usd < token8low and gelukt2 == "sell"):
                        print("Buying " + str(token8smallcasename) + ' (Current price: ' + str(pricetoken8usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token8smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token9address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1:
                    if (pricetoken9usd < token9low and gelukt == "sell") or (
                            pricetoken9usd < token9low and gelukt2 == "sell"):
                        print("Buying " + str(token9smallcasename) + ' (Current price: ' + str(pricetoken9usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token9smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
                if (token10address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1:
                    if (pricetoken10usd < token10low and gelukt == "sell") or (
                            pricetoken10usd < token10low and gelukt2 == "sell"):
                        print("Buying " + str(token10smallcasename) + ' (Current price: ' + str(pricetoken10usd) + ')')
                        if maincoinoption != '0x0000000000000000000000000000000000000000':
                            sellsmallcasesymbol = str(
                                cg.get_coin_info_from_contract_address_by_id(contract_address=ethaddress,
                                                                             id='ethereum')['symbol'])
                        else:
                            sellsmallcasesymbol = 'eth'
                            selldecimals = 18
                        kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=ethaddress,
                                         my_address=my_address,
                                         pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                         buysmallcasesymbol=token10smallcasename,
                                         sellsmallcasesymbol=sellsmallcasesymbol, ethtokeep=ethtokeep, speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                        time.sleep(timesleepaftertrade)
                        gelukt = kaka['gelukt']
                        keer = 9999
            except Exception as e:
                o = 0
                print(e)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                traceback.print_exc()
                if configfile.debugmode == '1':
                    print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                gelukt = "mislukt"
            try:  # token to token
                if token1address != 0:
                    try:  # token1 to others
                        if (token1address != 0) and (
                                token2address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token1totoken2 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken2 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token3address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token1totoken3 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken3 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token4address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token1totoken4 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken4 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token5address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token1totoken5 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken5 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token6address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token1totoken6 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken6 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token7address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token1totoken7 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken7 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token8address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token1totoken8 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken8 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token9address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token1totoken9 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken9 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token1address != 0) and (
                                token10address != 0) and activatetoken1 == 1 and tradewithETHtoken1 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken1 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token1totoken10 > tokentokennumerator and gelukt == "buy " + token1smallcasename) or (
                                    token1totoken10 > tokentokennumerator and gelukt2 == "buy " + token1smallcasename):
                                print("Trading " + str(token1smallcasename) + ' ($' + str(
                                    pricetoken1usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token1address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token1smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token2address != 0:
                    try:  # token2 to others
                        if (token2address != 0) and (
                                token1address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token2totoken1 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken1 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token3address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token2totoken3 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken3 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token4address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token2totoken4 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken4 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token5address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token2totoken5 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken5 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token6address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token2totoken6 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken6 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token7address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token2totoken7 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken7 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token8address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token2totoken8 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken8 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token9address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token2totoken9 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken9 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token2address != 0) and (
                                token10address != 0) and activatetoken2 == 1 and tradewithETHtoken2 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken2 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token2totoken10 > tokentokennumerator and gelukt == "buy " + token2smallcasename) or (
                                    token2totoken10 > tokentokennumerator and gelukt2 == "buy " + token2smallcasename):
                                print("Trading " + str(token2smallcasename) + ' ($' + str(
                                    pricetoken2usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token2address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token2smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token3address != 0:
                    try:  # token3 to others
                        if (token3address != 0) and (
                                token1address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token3totoken1 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken1 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token2address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token3totoken2 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken2 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token4address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token3totoken4 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken4 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token5address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token3totoken5 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken5 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token6address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token3totoken6 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken6 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token7address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token3totoken7 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken7 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token8address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token3totoken8 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken8 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token9address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token3totoken9 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken9 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token3address != 0) and (
                                token10address != 0) and activatetoken3 == 1 and tradewithETHtoken3 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken3 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token3totoken10 > tokentokennumerator and gelukt == "buy " + token3smallcasename) or (
                                    token3totoken10 > tokentokennumerator and gelukt2 == "buy " + token3smallcasename):
                                print("Trading " + str(token3smallcasename) + ' ($' + str(
                                    pricetoken3usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token3address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token3smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token4address != 0:
                    try:  # token4 to others
                        if (token4address != 0) and (
                                token2address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token4totoken2 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken2 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token1address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token4totoken1 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken1 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token3address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token4totoken3 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken3 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token5address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token4totoken5 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken5 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token6address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token4totoken6 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken6 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token7address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token4totoken7 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken7 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token8address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token4totoken8 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken8 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token9address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token4totoken9 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken9 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token4address != 0) and (
                                token10address != 0) and activatetoken4 == 1 and tradewithETHtoken4 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken4 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token4totoken10 > tokentokennumerator and gelukt == "buy " + token4smallcasename) or (
                                    token4totoken10 > tokentokennumerator and gelukt2 == "buy " + token4smallcasename):
                                print("Trading " + str(token4smallcasename) + ' ($' + str(
                                    pricetoken4usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token4address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token4smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token5address != 0:
                    try:  # token5 to others
                        if (token5address != 0) and (
                                token2address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token5totoken2 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken2 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token3address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token5totoken3 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken3 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token1address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token5totoken1 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken1 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token4address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token5totoken4 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken4 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token6address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token5totoken6 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken6 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token7address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token5totoken7 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken7 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token8address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token5totoken8 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken8 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token9address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token5totoken9 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken9 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token5address != 0) and (
                                token10address != 0) and activatetoken5 == 1 and tradewithETHtoken5 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken5 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token5totoken10 > tokentokennumerator and gelukt == "buy " + token5smallcasename) or (
                                    token5totoken10 > tokentokennumerator and gelukt2 == "buy " + token5smallcasename):
                                print("Trading " + str(token5smallcasename) + ' ($' + str(
                                    pricetoken5usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token5address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token5smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token6address != 0:
                    try:  # token6 to others
                        if (token6address != 0) and (
                                token2address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token6totoken2 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken2 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token3address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token6totoken3 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken3 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token4address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token6totoken4 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken4 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token1address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token6totoken1 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken1 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token5address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token6totoken5 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken5 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token7address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token6totoken7 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken7 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token8address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token6totoken8 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken8 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token9address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token6totoken9 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken9 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token6address != 0) and (
                                token10address != 0) and activatetoken6 == 1 and tradewithETHtoken6 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken6 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token6totoken10 > tokentokennumerator and gelukt == "buy " + token6smallcasename) or (
                                    token6totoken10 > tokentokennumerator and gelukt2 == "buy " + token6smallcasename):
                                print("Trading " + str(token6smallcasename) + ' ($' + str(
                                    pricetoken6usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token6address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token6smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token7address != 0:
                    try:  # token7 to others
                        if (token7address != 0) and (
                                token2address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token7totoken2 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken2 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token3address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token7totoken3 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken3 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token4address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token7totoken4 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken4 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token5address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token7totoken5 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken5 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token1address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token7totoken1 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken1 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token6address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token7totoken6 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken6 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token8address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token7totoken8 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken8 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token9address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token7totoken9 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken9 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token7address != 0) and (
                                token10address != 0) and activatetoken7 == 1 and tradewithETHtoken7 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken7 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token7totoken10 > tokentokennumerator and gelukt == "buy " + token7smallcasename) or (
                                    token7totoken10 > tokentokennumerator and gelukt2 == "buy " + token7smallcasename):
                                print("Trading " + str(token7smallcasename) + ' ($' + str(
                                    pricetoken7usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token7address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token7smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token8address != 0:
                    try:  # token8 to others
                        if (token8address != 0) and (
                                token2address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token8totoken2 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken2 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token3address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token8totoken3 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken3 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token4address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token8totoken4 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken4 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token5address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token8totoken5 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken5 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token6address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token8totoken6 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken6 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token1address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token8totoken1 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken1 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token7address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token8totoken7 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken7 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token9address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token8totoken9 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken9 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token8address != 0) and (
                                token10address != 0) and activatetoken8 == 1 and tradewithETHtoken8 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken8 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token8totoken10 > tokentokennumerator and gelukt == "buy " + token8smallcasename) or (
                                    token8totoken10 > tokentokennumerator and gelukt2 == "buy " + token8smallcasename):
                                print("Trading " + str(token8smallcasename) + ' ($' + str(
                                    pricetoken8usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token8address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token8smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token9address != 0:
                    try:  # token9 to others
                        if (token9address != 0) and (
                                token2address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token9totoken2 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken2 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token3address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token9totoken3 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken3 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token4address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token9totoken4 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken4 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token5address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token9totoken5 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken5 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token6address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token9totoken6 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken6 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token7address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token9totoken7 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken7 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token8address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token9totoken8 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken8 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token1address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token9totoken1 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken1 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token9address != 0) and (
                                token10address != 0) and activatetoken9 == 1 and tradewithETHtoken9 == 1 \
                                and activatetoken10 == 1 and tradewithETHtoken10 == 1 and tradewithERCtoken9 == 1 and tradewithERCtoken10 == 1:
                            if (
                                    token9totoken10 > tokentokennumerator and gelukt == "buy " + token9smallcasename) or (
                                    token9totoken10 > tokentokennumerator and gelukt2 == "buy " + token9smallcasename):
                                print("Trading " + str(token9smallcasename) + ' ($' + str(
                                    pricetoken9usd) + ') for ' + str(token10smallcasename) + " ($" + str(
                                    pricetoken10usd) + ")")

                                kaka = makeTrade(buytokenaddress=token10address, selltokenaddress=token9address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token10smallcasename,
                                                 sellsmallcasesymbol=token9smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
                if token10address != 0:
                    try:  # token10 to others
                        if (token10address != 0) and (
                                token2address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken2 == 1 and tradewithETHtoken2 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken2 == 1:
                            if (
                                    token10totoken2 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken2 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token2smallcasename) + " ($" + str(
                                    pricetoken2usd) + ")")

                                kaka = makeTrade(buytokenaddress=token2address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token2smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token3address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken3 == 1 and tradewithETHtoken3 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken3 == 1:
                            if (
                                    token10totoken3 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken3 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token3smallcasename) + " ($" + str(
                                    pricetoken3usd) + ")")

                                kaka = makeTrade(buytokenaddress=token3address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token3smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token4address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken4 == 1 and tradewithETHtoken4 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken4 == 1:
                            if (
                                    token10totoken4 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken4 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token4smallcasename) + " ($" + str(
                                    pricetoken4usd) + ")")

                                kaka = makeTrade(buytokenaddress=token4address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token4smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token5address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken5 == 1 and tradewithETHtoken5 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken5 == 1:
                            if (
                                    token10totoken5 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken5 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token5smallcasename) + " ($" + str(
                                    pricetoken5usd) + ")")

                                kaka = makeTrade(buytokenaddress=token5address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token5smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token6address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken6 == 1 and tradewithETHtoken6 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken6 == 1:
                            if (
                                    token10totoken6 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken6 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token6smallcasename) + " ($" + str(
                                    pricetoken6usd) + ")")

                                kaka = makeTrade(buytokenaddress=token6address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token6smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token7address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken7 == 1 and tradewithETHtoken7 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken7 == 1:
                            if (
                                    token10totoken7 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken7 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token7smallcasename) + " ($" + str(
                                    pricetoken7usd) + ")")

                                kaka = makeTrade(buytokenaddress=token7address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token7smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token8address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken8 == 1 and tradewithETHtoken8 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken8 == 1:
                            if (
                                    token10totoken8 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken8 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token8smallcasename) + " ($" + str(
                                    pricetoken8usd) + ")")

                                kaka = makeTrade(buytokenaddress=token8address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token8smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token1address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken1 == 1 and tradewithETHtoken1 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken1 == 1:
                            if (
                                    token10totoken1 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken1 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token1smallcasename) + " ($" + str(
                                    pricetoken1usd) + ")")

                                kaka = makeTrade(buytokenaddress=token1address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token1smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                        if (token10address != 0) and (
                                token9address != 0) and activatetoken10 == 1 and tradewithETHtoken10 == 1 \
                                and activatetoken9 == 1 and tradewithETHtoken9 == 1 and tradewithERCtoken10 == 1 and tradewithERCtoken9 == 1:
                            if (
                                    token10totoken9 > tokentokennumerator and gelukt == "buy " + token10smallcasename) or (
                                    token10totoken9 > tokentokennumerator and gelukt2 == "buy " + token10smallcasename):
                                print("Trading " + str(token10smallcasename) + ' ($' + str(
                                    pricetoken10usd) + ') for ' + str(token9smallcasename) + " ($" + str(
                                    pricetoken9usd) + ")")

                                kaka = makeTrade(buytokenaddress=token9address, selltokenaddress=token10address,
                                                 my_address=my_address,
                                                 pk=my_pk, max_slippage=max_slippage, infura_url=infura_url,
                                                 buysmallcasesymbol=token9smallcasename,
                                                 sellsmallcasesymbol=token10smallcasename, ethtokeep=ethtokeep,
                                                 speed=speed,maxgwei=maxgwei,maxgweinumber=maxgweinumber,diffdeposit=diffdeposit,diffdepositaddress=diffdepositaddress,ethaddress=ethaddress)
                                time.sleep(timesleepaftertrade)
                                gelukt = kaka['gelukt']
                                keer = 9999
                    except Exception as e:
                        o = 0
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        gelukt = "mislukt"
            except Exception as e:
                o = 0
                gelukt = "mislukt"
            if 'keer' not in locals():
                keer = keer2
            return {'gelukt': gelukt, 'keer': keer, 'fasttoken1': fasttoken1, 'fasttoken2': fasttoken2,
                    'fasttoken3': fasttoken3, 'fasttoken4': fasttoken4, 'fasttoken5': fasttoken5,
                    'fasttoken6': fasttoken6, 'fasttoken7': fasttoken7, 'fasttoken8': fasttoken8,
                    'fasttoken9': fasttoken9, 'fasttoken10': fasttoken10}

        def checkbalance(infura_url, my_address, token1address, token2address, token3address, token4address,
                         token5address,
                         token6address, token7address, token8address, token9address, token10address, maincoinoption,
                         token1decimals, token2decimals, token3decimals, token4decimals, token5decimals, token6decimals,
                         token7decimals, token8decimals, token9decimals, token10decimals):
            ethereum_address = my_address
            cg = CoinGeckoAPI()

            def api(ethaddress):
                time.sleep(200 / 1000)
                res = requests.get(
                    'https://api.ethplorer.io/getTokenInfo/' + ethaddress + '?apiKey=EK-5nuDS-iZCPJhW-SYGLU')
                data = int((res.json())["decimals"])
                return data

            ethbalance = pyetherbalance.PyEtherBalance(infura_url)
            try:
                token1smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token1address, id='ethereum')[
                        'symbol']
                token2smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token2address, id='ethereum')[
                        'symbol']
                token3smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token3address, id='ethereum')[
                        'symbol']
                token4smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token4address, id='ethereum')[
                        'symbol']
                token5smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token5address, id='ethereum')[
                        'symbol']
                token6smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token6address, id='ethereum')[
                        'symbol']
                token7smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token7address, id='ethereum')[
                        'symbol']
                token8smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token8address, id='ethereum')[
                        'symbol']
                token9smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token9address, id='ethereum')[
                        'symbol']
                token10smallcasename = \
                    cg.get_coin_info_from_contract_address_by_id(contract_address=token10address, id='ethereum')[
                        'symbol']
            except:
                o = 0
            try:
                balance_token1 = -1
                balance_token2 = -1
                balance_token3 = -1
                balance_token4 = -1
                balance_token5 = -1
                balance_token6 = -1
                balance_token7 = -1
                balance_token8 = -1
                balance_token9 = -1
                balance_token10 = -1
                maintokenbalance = -1
            except:
                o = 0

            try:
                if maincoinoption == "0x0000000000000000000000000000000000000000":
                    ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                    balance_eth = ethbalance.get_eth_balance(my_address)
                    ethamount2 = (float(balance_eth['balance']))
                else:
                    token2 = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                              id='ethereum')[
                                     'symbol']).upper
                    token2lower = str(
                        cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                     id='ethereum')[
                            'symbol'])
                    if maincoinoption == "0xdac17f958d2ee523a2206206994597c13d831ec7":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x6b175474e89094c44da98b954eedeac495271d0f":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
                        selldecimals = int(api(maincoinoption))
                    details2 = {'symbol': token2lower, 'address': maincoinoption,
                                'decimals': selldecimals,
                                'name': token2}
                    erc20tokens2 = ethbalance.add_token(token2, details2)
                    ethamount2 = math.floor(
                        ethbalance.get_token_balance(token2, ethereum_address)['balance'])
                maintokenbalance = ethamount2
                if (maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01) or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1):
                    gelukt = "sell"
                if 1==1:
                    token = token1smallcasename.upper
                    details = {'symbol': token, 'address': token1address, 'decimals': token1decimals,
                               'name': token}
                    erc20tokens = ethbalance.add_token(token, details)
                    balance_token1 = math.floor(ethbalance.get_token_balance(token, ethereum_address)['balance'])
                    if balance_token1 > 3:
                        gelukt = "buy " + token1smallcasename
                    if balance_token1 < 3 and str(token2address) != '0':
                        token = token2smallcasename.upper
                        details = {'symbol': token, 'address': token2address, 'decimals': token2decimals,
                                   'name': token}
                        erc20tokens = ethbalance.add_token(token, details)
                        balance_token2 = math.floor(
                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                        if balance_token2 > 3:
                            gelukt = "buy " + token2smallcasename
                        if balance_token2 < 3 and str(token3address) != '0':
                            token = (token3smallcasename).upper
                            details = {'symbol': token, 'address': token3address, 'decimals': token3decimals,
                                       'name': token}

                            erc20tokens = ethbalance.add_token(token, details)
                            balance_token3 = math.floor(
                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                            if balance_token3 > 3:
                                gelukt = "buy " + token3smallcasename
                            if balance_token3 < 3 and str(token4address) != '0':
                                token = token4smallcasename.upper
                                details = {'symbol': token, 'address': token4address, 'decimals': token4decimals,
                                           'name': token}
                                erc20tokens = ethbalance.add_token(token, details)
                                balance_token4 = math.floor(
                                    ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                if balance_token4 > 3:
                                    gelukt = "buy " + token4smallcasename
                                if balance_token4 < 3 and str(token5address) != '0':
                                    token = token5smallcasename.upper
                                    details = {'symbol': token, 'address': token5address, 'decimals': token5decimals,
                                               'name': token}
                                    erc20tokens = ethbalance.add_token(token, details)
                                    balance_token5 = math.floor(
                                        ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                    if balance_token5 > 3:
                                        gelukt = "buy " + token5smallcasename
                                    if balance_token5 < 3 and str(token6address) != '0':
                                        token = token6smallcasename.upper
                                        details = {'symbol': token, 'address': token6address,
                                                   'decimals': token6decimals,
                                                   'name': token}
                                        erc20tokens = ethbalance.add_token(token, details)
                                        balance_token6 = math.floor(
                                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                        if balance_token6 > 3:
                                            gelukt = "buy " + token6smallcasename
                                        if balance_token6 < 3 and str(token7address) != '0':
                                            token = token7smallcasename.upper
                                            details = {'symbol': token, 'address': token7address,
                                                       'decimals': token7decimals,
                                                       'name': token}
                                            erc20tokens = ethbalance.add_token(token, details)
                                            balance_token7 = math.floor(
                                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                            if balance_token7 > 3:
                                                gelukt = "buy " + token7smallcasename
                                            if balance_token7 < 3 and str(token8address) != '0':
                                                token = token8smallcasename.upper
                                                details = {'symbol': token, 'address': token8address,
                                                           'decimals': token8decimals,
                                                           'name': token}
                                                erc20tokens = ethbalance.add_token(token, details)
                                                balance_token8 = math.floor(
                                                    ethbalance.get_token_balance(token, ethereum_address)[
                                                        'balance'])
                                                if balance_token8 > 3:
                                                    gelukt = "buy " + token8smallcasename
                                                if balance_token8 < 3 and str(token9address) != '0':
                                                    token = token9smallcasename.upper
                                                    details = {'symbol': token, 'address': token9address,
                                                               'decimals': token9decimals,
                                                               'name': token}
                                                    erc20tokens = ethbalance.add_token(token, details)
                                                    balance_token9 = math.floor(
                                                        ethbalance.get_token_balance(token, ethereum_address)[
                                                            'balance'])
                                                    if balance_token9 > 3:
                                                        gelukt = "buy " + token9smallcasename
                                                    if balance_token9 < 3 and str(token10address) != '0':
                                                        token = token10smallcasename.upper
                                                        details = {'symbol': token, 'address': token10address,
                                                                   'decimals': token10decimals,
                                                                   'name': token}
                                                        erc20tokens = ethbalance.add_token(token, details)
                                                        balance_token10 = math.floor(
                                                            ethbalance.get_token_balance(token, ethereum_address)[
                                                                'balance'])
                                                        if balance_token10 > 3:
                                                            gelukt = "buy " + token10smallcasename
                keer = 0
                if 'gelukt' not in locals():
                    gelukt = 'nothing'
            except Exception as e:
                o = 0
                time.sleep(5)
                if maincoinoption == "0x0000000000000000000000000000000000000000":
                    ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                    balance_eth = ethbalance.get_eth_balance(my_address)
                    ethamount2 = (float(balance_eth['balance']))
                else:
                    token2 = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                              id='ethereum')[
                                     'symbol']).upper
                    token2lower = str(
                        cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                     id='ethereum')[
                            'symbol'])
                    if maincoinoption == "0xdac17f958d2ee523a2206206994597c13d831ec7":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x6b175474e89094c44da98b954eedeac495271d0f":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
                        selldecimals = int(api(maincoinoption))
                    details2 = {'symbol': token2lower, 'address': maincoinoption,
                                'decimals': selldecimals,
                                'name': token2}
                    erc20tokens2 = ethbalance.add_token(token2, details2)
                    ethamount2 = math.floor(
                        ethbalance.get_token_balance(token2, ethereum_address)['balance'])
                maintokenbalance = ethamount2
                if (maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01) or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1):
                    gelukt = "sell"
                if 1==1:
                    token = token1smallcasename.upper
                    details = {'symbol': token, 'address': token1address, 'decimals': token1decimals,
                               'name': token}
                    erc20tokens = ethbalance.add_token(token, details)
                    balance_token1 = math.floor(ethbalance.get_token_balance(token, ethereum_address)['balance'])
                    if balance_token1 > 3:
                        gelukt = "buy " + token1smallcasename
                    if balance_token1 < 3 and str(token2address) != '0':
                        token = token2smallcasename.upper
                        details = {'symbol': token, 'address': token2address, 'decimals': token2decimals,
                                   'name': token}
                        erc20tokens = ethbalance.add_token(token, details)
                        balance_token2 = math.floor(
                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                        if balance_token2 > 3:
                            gelukt = "buy " + token2smallcasename
                        if balance_token2 < 3 and str(token3address) != '0':
                            token = (token3smallcasename).upper
                            details = {'symbol': token, 'address': token3address, 'decimals': token3decimals,
                                       'name': token}

                            erc20tokens = ethbalance.add_token(token, details)
                            balance_token3 = math.floor(
                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                            if balance_token3 > 3:
                                gelukt = "buy " + token3smallcasename
                            if balance_token3 < 3 and str(token4address) != '0':
                                token = token4smallcasename.upper
                                details = {'symbol': token, 'address': token4address, 'decimals': token4decimals,
                                           'name': token}
                                erc20tokens = ethbalance.add_token(token, details)
                                balance_token4 = math.floor(
                                    ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                if balance_token4 > 3:
                                    gelukt = "buy " + token4smallcasename
                                if balance_token4 < 3 and str(token5address) != '0':
                                    token = token5smallcasename.upper
                                    details = {'symbol': token, 'address': token5address, 'decimals': token5decimals,
                                               'name': token}
                                    erc20tokens = ethbalance.add_token(token, details)
                                    balance_token5 = math.floor(
                                        ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                    if balance_token5 > 3:
                                        gelukt = "buy " + token5smallcasename
                                    if balance_token5 < 3 and str(token6address) != '0':
                                        token = token6smallcasename.upper
                                        details = {'symbol': token, 'address': token6address,
                                                   'decimals': token6decimals,
                                                   'name': token}
                                        erc20tokens = ethbalance.add_token(token, details)
                                        balance_token6 = math.floor(
                                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                        if balance_token6 > 3:
                                            gelukt = "buy " + token6smallcasename
                                        if balance_token6 < 3 and str(token7address) != '0':
                                            token = token7smallcasename.upper
                                            details = {'symbol': token, 'address': token7address,
                                                       'decimals': token7decimals,
                                                       'name': token}
                                            erc20tokens = ethbalance.add_token(token, details)
                                            balance_token7 = math.floor(
                                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                            if balance_token7 > 3:
                                                gelukt = "buy " + token7smallcasename
                                            if balance_token7 < 3 and str(token8address) != '0':
                                                token = token8smallcasename.upper
                                                details = {'symbol': token, 'address': token8address,
                                                           'decimals': token8decimals,
                                                           'name': token}
                                                erc20tokens = ethbalance.add_token(token, details)
                                                balance_token8 = math.floor(
                                                    ethbalance.get_token_balance(token, ethereum_address)[
                                                        'balance'])
                                                if balance_token8 > 3:
                                                    gelukt = "buy " + token8smallcasename
                                                if balance_token8 < 3 and str(token9address) != '0':
                                                    token = token9smallcasename.upper
                                                    details = {'symbol': token, 'address': token9address,
                                                               'decimals': token9decimals,
                                                               'name': token}
                                                    erc20tokens = ethbalance.add_token(token, details)
                                                    balance_token9 = math.floor(
                                                        ethbalance.get_token_balance(token, ethereum_address)[
                                                            'balance'])
                                                    if balance_token9 > 3:
                                                        gelukt = "buy " + token9smallcasename
                                                    if balance_token9 < 3 and str(token10address) != '0':
                                                        token = token10smallcasename.upper
                                                        details = {'symbol': token, 'address': token10address,
                                                                   'decimals': token10decimals,
                                                                   'name': token}
                                                        erc20tokens = ethbalance.add_token(token, details)
                                                        balance_token10 = math.floor(
                                                            ethbalance.get_token_balance(token, ethereum_address)[
                                                                'balance'])
                                                        if balance_token10 > 3:
                                                            gelukt = "buy " + token10smallcasename
                keer = 0
                if 'gelukt' not in locals():
                    gelukt = 'nothing'

            try:
                if maincoinoption == "0x0000000000000000000000000000000000000000":
                    ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                    balance_eth = ethbalance.get_eth_balance(my_address)
                    ethamount2 = (float(balance_eth['balance']))
                else:
                    token2 = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                              id='ethereum')[
                                     'symbol']).upper
                    token2lower = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                                   id='ethereum')[
                                          'symbol'])
                    if maincoinoption == "0xdac17f958d2ee523a2206206994597c13d831ec7":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x6b175474e89094c44da98b954eedeac495271d0f":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
                        selldecimals = int(api(maincoinoption))
                    details2 = {'symbol': token2lower, 'address': maincoinoption,
                                'decimals': selldecimals,
                                'name': token2}
                    erc20tokens2 = ethbalance.add_token(token2, details2)
                    ethamount2 = math.floor(
                        ethbalance.get_token_balance(token2, ethereum_address)['balance'])
                if (
                        maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01 and gelukt != "sell") or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1 and gelukt != "sell"):
                    gelukt2 = "sell"
                if (
                        maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01 and gelukt == "sell") or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1 and gelukt == "sell"):
                    gelukt2 = "nothing"
                    ethamount2 = 0.05
                if (ethamount2 < 0.01 and maincoinoption == "0x0000000000000000000000000000000000000000") or (
                        ethamount2 < 1 and maincoinoption != "0x0000000000000000000000000000000000000000"):
                    token = token1smallcasename.upper
                    details = {'symbol': token, 'address': token1address, 'decimals': token1decimals,
                               'name': token}
                    erc20tokens = ethbalance.add_token(token, details)
                    balance_token1 = math.floor(ethbalance.get_token_balance(token, ethereum_address)['balance'])
                    if balance_token1 > 3 and gelukt != ("buy " + str(token1smallcasename)):
                        gelukt2 = "buy " + token1smallcasename
                    if balance_token1 < 3 and str(token2address) != '0' or (
                            balance_token1 > 3 and gelukt == ("buy " + str(token1smallcasename)) and str(
                        token2address) != '0'):
                        token = token2smallcasename.upper
                        details = {'symbol': token, 'address': token2address, 'decimals': token2decimals,
                                   'name': token}
                        erc20tokens = ethbalance.add_token(token, details)
                        balance_token2 = math.floor(
                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                        if balance_token2 > 3 and (gelukt) != ("buy " + str(token2smallcasename)):
                            gelukt2 = "buy " + token2smallcasename
                        if balance_token2 < 3 and str(token3address) != '0' or (
                                balance_token2 > 3 and gelukt == ("buy " + str(token2smallcasename)) and str(
                            token3address) != '0'):
                            token = (token3smallcasename).upper
                            details = {'symbol': token, 'address': token3address, 'decimals': token3decimals,
                                       'name': token}
                            erc20tokens = ethbalance.add_token(token, details)
                            balance_token3 = math.floor(
                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                            if balance_token3 > 3 and (gelukt) != ("buy " + str(token3smallcasename)):
                                gelukt2 = "buy " + token3smallcasename
                            if balance_token3 < 3 and str(token4address) != '0' or (
                                    balance_token3 > 3 and gelukt == ("buy " + str(token3smallcasename)) and str(
                                token4address) != '0'):
                                token = token4smallcasename.upper
                                details = {'symbol': token, 'address': token4address, 'decimals': token4decimals,
                                           'name': token}
                                erc20tokens = ethbalance.add_token(token, details)
                                balance_token4 = math.floor(
                                    ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                if balance_token4 > 3 and (gelukt) != ("buy " + str(token4smallcasename)):
                                    gelukt2 = "buy " + token4smallcasename
                                if balance_token4 < 3 and str(token5address) != '0' or (
                                        balance_token4 > 3 and gelukt == ("buy " + str(token4smallcasename)) and str(
                                    token5address) != '0'):
                                    token = token5smallcasename.upper
                                    details = {'symbol': token, 'address': token5address, 'decimals': token5decimals,
                                               'name': token}
                                    erc20tokens = ethbalance.add_token(token, details)
                                    balance_token5 = math.floor(
                                        ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                    if balance_token5 > 3 and (gelukt) != ("buy " + str(token5smallcasename)):
                                        gelukt2 = "buy " + token5smallcasename
                                    if balance_token5 < 3 and str(token6address) != '0' or (
                                            balance_token5 > 3 and gelukt == (
                                            "buy " + str(token5smallcasename)) and str(token6address) != '0'):
                                        token = token6smallcasename.upper
                                        details = {'symbol': token, 'address': token6address,
                                                   'decimals': token6decimals,
                                                   'name': token}
                                        erc20tokens = ethbalance.add_token(token, details)
                                        balance_token6 = math.floor(
                                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                        if balance_token6 > 3 and (gelukt) != ("buy " + str(token5smallcasename)):
                                            gelukt2 = "buy " + token6smallcasename
                                        if balance_token6 < 3 and str(token7address) != '0' or (
                                                balance_token6 > 3 and gelukt == (
                                                "buy " + str(token6smallcasename)) and str(token7address) != '0'):
                                            token = token7smallcasename.upper
                                            details = {'symbol': token, 'address': token7address,
                                                       'decimals': token7decimals,
                                                       'name': token}
                                            erc20tokens = ethbalance.add_token(token, details)
                                            balance_token7 = math.floor(
                                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                            if balance_token7 > 3 and (gelukt) != (
                                                    "buy " + str(token6smallcasename)):
                                                gelukt2 = "buy " + token7smallcasename
                                            if balance_token7 < 3 and str(token8address) != '0' or (
                                                    balance_token7 > 3 and gelukt == (
                                                    "buy " + str(token7smallcasename)) and str(token8address) != '0'):
                                                token = token8smallcasename.upper
                                                details = {'symbol': token, 'address': token8address,
                                                           'decimals': token8decimals,
                                                           'name': token}
                                                erc20tokens = ethbalance.add_token(token, details)
                                                balance_token8 = math.floor(
                                                    ethbalance.get_token_balance(token, ethereum_address)[
                                                        'balance'])
                                                if balance_token8 > 3 and (gelukt) != (
                                                        "buy " + str(token8smallcasename)):
                                                    gelukt2 = "buy " + token8smallcasename
                                                if balance_token8 < 3 and str(token9address) != '0' or (
                                                        balance_token8 > 3 and gelukt == (
                                                        "buy " + str(token8smallcasename)) and str(
                                                    token9address) != '0'):
                                                    token = token9smallcasename.upper
                                                    details = {'symbol': token, 'address': token9address,
                                                               'decimals': token9decimals,
                                                               'name': token}
                                                    erc20tokens = ethbalance.add_token(token, details)
                                                    balance_token9 = math.floor(
                                                        ethbalance.get_token_balance(token, ethereum_address)[
                                                            'balance'])
                                                    if balance_token9 > 3 and (gelukt) != (
                                                            "buy " + str(token9smallcasename)):
                                                        gelukt2 = "buy " + token9smallcasename
                                                    if balance_token9 < 3 and str(token10address) != '0' and (
                                                            gelukt) != (
                                                            "buy " + str(token10smallcasename)) or (
                                                            balance_token9 > 3 and gelukt == (
                                                            "buy " + str(token9smallcasename)) and str(
                                                        token10address) != '0'):
                                                        token = token10smallcasename.upper
                                                        details = {'symbol': token, 'address': token10address,
                                                                   'decimals': token10decimals,
                                                                   'name': token}
                                                        erc20tokens = ethbalance.add_token(token, details)
                                                        balance_token10 = math.floor(
                                                            ethbalance.get_token_balance(token, ethereum_address)[
                                                                'balance'])
                                                        if balance_token10 > 3:
                                                            gelukt2 = "buy " + token10smallcasename
                if 'gelukt2' not in locals():
                    gelukt2 = 'nothing'

            except Exception as e:
                o = 0
                time.sleep(3)
                if maincoinoption == "0x0000000000000000000000000000000000000000":
                    ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                    balance_eth = ethbalance.get_eth_balance(my_address)
                    ethamount2 = (float(balance_eth['balance']))
                else:
                    token2 = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                              id='ethereum')[
                                     'symbol']).upper
                    token2lower = str(cg.get_coin_info_from_contract_address_by_id(contract_address=maincoinoption,
                                                                                   id='ethereum')[
                                          'symbol'])
                    if maincoinoption == "0xdac17f958d2ee523a2206206994597c13d831ec7":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x6b175474e89094c44da98b954eedeac495271d0f":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599":
                        selldecimals = int(api(maincoinoption))
                    if maincoinoption == '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2':
                        selldecimals = int(api(maincoinoption))
                    details2 = {'symbol': token2lower, 'address': maincoinoption,
                                'decimals': selldecimals,
                                'name': token2}
                    erc20tokens2 = ethbalance.add_token(token2, details2)
                    ethamount2 = math.floor(
                        ethbalance.get_token_balance(token2, ethereum_address)['balance'])
                if (
                        maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01 and gelukt != "sell") or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1 and gelukt != "sell"):
                    gelukt2 = "sell"
                if (
                        maincoinoption == "0x0000000000000000000000000000000000000000" and ethamount2 > 0.01 and gelukt == "sell") or (
                        maincoinoption != "0x0000000000000000000000000000000000000000" and ethamount2 > 1 and gelukt == "sell"):
                    gelukt2 = "nothing"
                    ethamount2 = 0.05
                if (ethamount2 < 0.01 and maincoinoption == "0x0000000000000000000000000000000000000000") or (
                        ethamount2 < 1 and maincoinoption != "0x0000000000000000000000000000000000000000"):
                    token = token1smallcasename.upper
                    details = {'symbol': token, 'address': token1address, 'decimals': token1decimals,
                               'name': token}
                    erc20tokens = ethbalance.add_token(token, details)
                    balance_token1 = math.floor(ethbalance.get_token_balance(token, ethereum_address)['balance'])
                    if balance_token1 > 3 and gelukt != ("buy " + str(token1smallcasename)):
                        gelukt2 = "buy " + token1smallcasename
                    if balance_token1 < 3 and str(token2address) != '0' or (
                            balance_token1 > 3 and gelukt == ("buy " + str(token1smallcasename)) and str(
                        token2address) != '0'):
                        token = token2smallcasename.upper
                        details = {'symbol': token, 'address': token2address, 'decimals': token2decimals,
                                   'name': token}
                        erc20tokens = ethbalance.add_token(token, details)
                        balance_token2 = math.floor(
                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                        if balance_token2 > 3 and (gelukt) != ("buy " + str(token2smallcasename)):
                            gelukt2 = "buy " + token2smallcasename
                        if balance_token2 < 3 and str(token3address) != '0' or (
                                balance_token2 > 3 and gelukt == ("buy " + str(token2smallcasename)) and str(
                            token3address) != '0'):
                            token = (token3smallcasename).upper
                            details = {'symbol': token, 'address': token3address, 'decimals': token3decimals,
                                       'name': token}
                            erc20tokens = ethbalance.add_token(token, details)
                            balance_token3 = math.floor(
                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                            if balance_token3 > 3 and (gelukt) != ("buy " + str(token3smallcasename)):
                                gelukt2 = "buy " + token3smallcasename
                            if balance_token3 < 3 and str(token4address) != '0' or (
                                    balance_token3 > 3 and gelukt == ("buy " + str(token3smallcasename)) and str(
                                token4address) != '0'):
                                token = token4smallcasename.upper
                                details = {'symbol': token, 'address': token4address, 'decimals': token4decimals,
                                           'name': token}
                                erc20tokens = ethbalance.add_token(token, details)
                                balance_token4 = math.floor(
                                    ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                if balance_token4 > 3 and (gelukt) != ("buy " + str(token4smallcasename)):
                                    gelukt2 = "buy " + token4smallcasename
                                if balance_token4 < 3 and str(token5address) != '0' or (
                                        balance_token4 > 3 and gelukt == (
                                        "buy " + str(token4smallcasename)) and str(token5address) != '0'):
                                    token = token5smallcasename.upper
                                    details = {'symbol': token, 'address': token5address, 'decimals': token5decimals,
                                               'name': token}
                                    erc20tokens = ethbalance.add_token(token, details)
                                    balance_token5 = math.floor(
                                        ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                    if balance_token5 > 3 and (gelukt) != ("buy " + str(token5smallcasename)):
                                        gelukt2 = "buy " + token5smallcasename
                                    if balance_token5 < 3 and str(token6address) != '0' or (
                                            balance_token5 > 3 and gelukt == (
                                            "buy " + str(token5smallcasename)) and str(token6address) != '0'):
                                        token = token6smallcasename.upper
                                        details = {'symbol': token, 'address': token6address,
                                                   'decimals': token6decimals,
                                                   'name': token}
                                        erc20tokens = ethbalance.add_token(token, details)
                                        balance_token6 = math.floor(
                                            ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                        if balance_token6 > 3 and (gelukt) != ("buy " + str(token5smallcasename)):
                                            gelukt2 = "buy " + token6smallcasename
                                        if balance_token6 < 3 and str(token7address) != '0' or (
                                                balance_token6 > 3 and gelukt == (
                                                "buy " + str(token6smallcasename)) and str(token7address) != '0'):
                                            token = token7smallcasename.upper
                                            details = {'symbol': token, 'address': token7address,
                                                       'decimals': token7decimals,
                                                       'name': token}
                                            erc20tokens = ethbalance.add_token(token, details)
                                            balance_token7 = math.floor(
                                                ethbalance.get_token_balance(token, ethereum_address)['balance'])
                                            if balance_token7 > 3 and (gelukt) != (
                                                    "buy " + str(token6smallcasename)):
                                                gelukt2 = "buy " + token7smallcasename
                                            if balance_token7 < 3 and str(token8address) != '0' or (
                                                    balance_token7 > 3 and gelukt == (
                                                    "buy " + str(token7smallcasename)) and str(
                                                token8address) != '0'):
                                                token = token8smallcasename.upper
                                                details = {'symbol': token, 'address': token8address,
                                                           'decimals': token8decimals,
                                                           'name': token}
                                                erc20tokens = ethbalance.add_token(token, details)
                                                balance_token8 = math.floor(
                                                    ethbalance.get_token_balance(token, ethereum_address)[
                                                        'balance'])
                                                if balance_token8 > 3 and (gelukt) != (
                                                        "buy " + str(token8smallcasename)):
                                                    gelukt2 = "buy " + token8smallcasename
                                                if balance_token8 < 3 and str(token9address) != '0' or (
                                                        balance_token8 > 3 and gelukt == (
                                                        "buy " + str(token8smallcasename)) and str(
                                                    token9address) != '0'):
                                                    token = token9smallcasename.upper
                                                    details = {'symbol': token, 'address': token9address,
                                                               'decimals': token9decimals,
                                                               'name': token}
                                                    erc20tokens = ethbalance.add_token(token, details)
                                                    balance_token9 = math.floor(
                                                        ethbalance.get_token_balance(token, ethereum_address)[
                                                            'balance'])
                                                    if balance_token9 > 3 and (gelukt) != (
                                                            "buy " + str(token9smallcasename)):
                                                        gelukt2 = "buy " + token9smallcasename
                                                    if balance_token9 < 3 and str(token10address) != '0' and (
                                                            gelukt) != (
                                                            "buy " + str(token10smallcasename)) or (
                                                            balance_token9 > 3 and gelukt == (
                                                            "buy " + str(token9smallcasename)) and str(
                                                        token10address) != '0'):
                                                        token = token10smallcasename.upper
                                                        details = {'symbol': token, 'address': token10address,
                                                                   'decimals': token10decimals,
                                                                   'name': token}
                                                        erc20tokens = ethbalance.add_token(token, details)
                                                        balance_token10 = math.floor(
                                                            ethbalance.get_token_balance(token, ethereum_address)[
                                                                'balance'])
                                                        if balance_token10 > 3:
                                                            gelukt2 = "buy " + token10smallcasename
                if 'gelukt2' not in locals():
                    gelukt2 = 'nothing'
            try:
                gelukt3 = gelukt2
            except:
                gelukt2 = '0'
            return {'keer': keer, 'gelukt': gelukt, 'gelukt2': gelukt2, 'balance_token1': balance_token1,
                    'balance_token2': balance_token2, 'balance_token3': balance_token3,
                    'balance_token4': balance_token4,
                    'balance_token5': balance_token5, 'balance_token6': balance_token6,
                    'balance_token7': balance_token7,
                    'balance_token8': balance_token8, 'balance_token9': balance_token9,
                    'balance_token10': balance_token10,
                    'maintokenbalance': maintokenbalance}

        def getprice(token1address, token1smallcasename, token2address, token2smallcasename, token3address,
                     token3smallcasename,
                     token4address, token4smallcasename, token5address, token5smallcasename, token6address,
                     token6smallcasename,
                     token7address, token7smallcasename, token8address, token8smallcasename, token9address,
                     token9smallcasename,
                     token10address, token10smallcasename, token1high, token1low, token2high, token2low, token3high,
                     token3low,
                     token4high, token4low, token5high, token5low, token6high, token6low, token7high, token7low,
                     token8high,
                     token8low, token9high, token9low, token10high, token10low, incaseofbuyinghowmuch,
                     uniswap_wrapper, timesleep, gelukt, token1decimals, token2decimals, token3decimals, token4decimals,
                     token5decimals, token6decimals, token7decimals, token8decimals, token9decimals, token10decimals,
                     activatetoken1, activatetoken2, activatetoken3, activatetoken4, activatetoken5, activatetoken6,
                     activatetoken7, activatetoken8, activatetoken9, activatetoken10, balance_token1,
                     balance_token2, balance_token3, balance_token4,
                     balance_token5, balance_token6, balance_token7,
                     balance_token8, balance_token9, balance_token10,
                     maintokenbalance, ethaddress, maindecimals):
            time.sleep(timesleep)
            time.sleep(1 / 6)
            threeeth = 10 ** 18 * 1 * incaseofbuyinghowmuch
            if 'buy' in gelukt:
                priceright = 'buy'
            else:
                priceright = 'sell'
            if priceright == 'sell':
                token1eth = uniswap_wrapper.get_eth_token_input_price(w33.toChecksumAddress(token1address),
                                                                      threeeth)
                token1eth2 = token1eth / threeeth
                priceeth = cg.get_price(ids='ethereum', vs_currencies='usd')
            else:
                token1eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(token1address),
                                                                       threeeth)
                token1eth2 = (token1eth / threeeth)
                priceeth = cg.get_price(ids='ethereum', vs_currencies='usd')
            if ethaddress == "0x0000000000000000000000000000000000000000":
                dollarbalancemaintoken = maintokenbalance * (priceeth['ethereum']['usd'])
            else:
                token11eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(ethaddress),
                                                                        threeeth)
                token11eth2 = token11eth / threeeth

                if maindecimals != 18:
                    dollarbalancemaintoken = maintokenbalance * ((priceeth['ethereum']['usd'] / (token11eth2)) / (
                            10 ** (18 - (maindecimals))))
                else:
                    dollarbalancemaintoken = maintokenbalance * (priceeth['ethereum']['usd'] / (token11eth2))

            try:
                pricetoken1usd = 0
                pricetoken2usd = 0
                pricetoken3usd = 0
                pricetoken4usd = 0
                pricetoken5usd = 0
                pricetoken6usd = 0
                pricetoken7usd = 0
                pricetoken8usd = 0
                pricetoken9usd = 0
                pricetoken10usd = 0
                dollarbalancetoken1 = 0
                dollarbalancetoken2 = 0
                dollarbalancetoken3 = 0
                dollarbalancetoken4 = 0
                dollarbalancetoken5 = 0
                dollarbalancetoken6 = 0
                dollarbalancetoken7 = 0
                dollarbalancetoken8 = 0
                dollarbalancetoken9 = 0
                dollarbalancetoken10 = 0
                dollarbalancemaintoken = 0



            except:
                o = 0
            try:
                if token1decimals != 18:
                    pricetoken1usd = (priceeth['ethereum']['usd'] / (token1eth2)) / (10 ** (18 - (token1decimals)))
                    dollarbalancetoken1 = pricetoken1usd * balance_token1
                else:
                    pricetoken1usd = (priceeth['ethereum']['usd'] / (token1eth2))
                dollarbalancetoken1 = pricetoken1usd * balance_token1
                if str(token2address) != '0':
                    if priceright == 'sell':
                        token2eth = uniswap_wrapper.get_eth_token_input_price(w33.toChecksumAddress(token2address),
                                                                              threeeth)
                        token2eth2 = (token2eth) / threeeth
                        if token2decimals != 18:
                            pricetoken2usd = (priceeth['ethereum']['usd'] / (token2eth2)) / (
                                    10 ** (18 - (token2decimals)))
                            dollarbalancetoken2 = pricetoken2usd * balance_token2
                        else:
                            pricetoken2usd = (priceeth['ethereum']['usd'] / (token2eth2))

                    else:
                        token2eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(token2address),
                                                                               threeeth)
                        token2eth2 = (token2eth) / threeeth
                    dollarbalancetoken2 = pricetoken2usd * balance_token2
                    if token2decimals != 18:
                        pricetoken2usd = (priceeth['ethereum']['usd'] / (token2eth2)) / (
                                10 ** (18 - (token2decimals)))
                        dollarbalancetoken2 = pricetoken2usd * balance_token2
                    else:
                        pricetoken2usd = (priceeth['ethereum']['usd'] / (token2eth2))
                dollarbalancetoken2 = pricetoken2usd * balance_token2
                if str(token3address) != '0':
                    if priceright == 'sell':
                        token3eth = uniswap_wrapper.get_eth_token_input_price(w33.toChecksumAddress(token3address),
                                                                              threeeth)
                        token3eth2 = token3eth / threeeth
                        if token3decimals != 18:
                            pricetoken3usd = (priceeth['ethereum']['usd'] / (token3eth2)) / (
                                    10 ** (18 - (token3decimals)))
                            dollarbalancetoken3 = pricetoken3usd * balance_token3
                        else:
                            pricetoken3usd = (priceeth['ethereum']['usd'] / (token3eth2))
                    else:
                        token3eth = uniswap_wrapper.get_token_eth_output_price(w33.toChecksumAddress(token3address),
                                                                               threeeth)
                        token3eth2 = token3eth / threeeth
                        if token3decimals != 18:
                            pricetoken3usd = (priceeth['ethereum']['usd'] / (token3eth2)) / (
                                    10 ** (18 - (token3decimals)))
                        else:
                            pricetoken3usd = (priceeth['ethereum']['usd'] / (token3eth2))
                    dollarbalancetoken3 = pricetoken3usd * balance_token3
                    if str(token4address) != '0':
                        if priceright == 'sell':
                            token4eth = uniswap_wrapper.get_eth_token_input_price(
                                w33.toChecksumAddress(token4address),
                                threeeth)
                            token4eth2 = token4eth / threeeth
                            if token4decimals != 18:
                                pricetoken4usd = (priceeth['ethereum']['usd'] / (token4eth2)) / (
                                        10 ** (18 - (token4decimals)))
                            else:
                                pricetoken4usd = (priceeth['ethereum']['usd'] / (token4eth2))
                        else:
                            token4eth = uniswap_wrapper.get_token_eth_output_price(
                                w33.toChecksumAddress(token4address),
                                threeeth)
                            token4eth2 = token4eth / threeeth
                            if token4decimals != 18:
                                pricetoken4usd = (priceeth['ethereum']['usd'] / (token4eth2)) / (
                                        10 ** (18 - (token4decimals)))
                            else:
                                pricetoken4usd = (priceeth['ethereum']['usd'] / (token4eth2))
                        dollarbalancetoken4 = pricetoken4usd * balance_token4
                        if str(token5address) != '0':
                            if priceright == 'sell':
                                token5eth = uniswap_wrapper.get_eth_token_input_price(
                                    w33.toChecksumAddress(token5address),
                                    threeeth)
                                token5eth2 = token5eth / threeeth
                                if token5decimals != 18:
                                    pricetoken5usd = (priceeth['ethereum']['usd'] / (token5eth2)) / (
                                            10 ** (18 - (token5decimals)))
                                else:
                                    pricetoken5usd = (priceeth['ethereum']['usd'] / (token5eth2))
                            else:
                                token5eth = uniswap_wrapper.get_token_eth_output_price(
                                    w33.toChecksumAddress(token5address),
                                    threeeth)
                                token5eth2 = token5eth / threeeth
                                if token5decimals != 18:
                                    pricetoken5usd = (priceeth['ethereum']['usd'] / (token5eth2)) / (
                                            10 ** (18 - (token5decimals)))
                                else:
                                    pricetoken5usd = (priceeth['ethereum']['usd'] / (token5eth2))
                            dollarbalancetoken5 = pricetoken5usd * balance_token5
                            if str(token6address) != '0':
                                if priceright == 'sell':
                                    token6eth = uniswap_wrapper.get_eth_token_input_price(
                                        w33.toChecksumAddress(token6address),
                                        threeeth)
                                    token6eth2 = token6eth / threeeth
                                    if token6decimals != 18:
                                        pricetoken6usd = (priceeth['ethereum']['usd'] / (token6eth2)) / (
                                                10 ** (18 - (token6decimals)))
                                    else:
                                        pricetoken6usd = (priceeth['ethereum']['usd'] / (token6eth2))
                                else:
                                    token6eth = uniswap_wrapper.get_token_eth_output_price(
                                        w33.toChecksumAddress(token6address),
                                        threeeth)
                                    token6eth2 = token6eth / threeeth
                                    if token6decimals != 18:
                                        pricetoken6usd = (priceeth['ethereum']['usd'] / (token6eth2)) / (
                                                10 ** (18 - (token6decimals)))
                                    else:
                                        pricetoken6usd = (priceeth['ethereum']['usd'] / (token6eth2))
                                dollarbalancetoken6 = pricetoken6usd * balance_token6
                                if str(token7address) != '0':
                                    if priceright == 'sell':
                                        token7eth = uniswap_wrapper.get_eth_token_input_price(
                                            w33.toChecksumAddress(token7address),
                                            threeeth)
                                        token7eth2 = token7eth / threeeth
                                        if token7decimals != 18:
                                            pricetoken7usd = (priceeth['ethereum']['usd'] / (token7eth2)) / (
                                                    10 ** (18 - (token7decimals)))
                                        else:
                                            pricetoken7usd = (priceeth['ethereum']['usd'] / (token7eth2))
                                    else:
                                        token7eth = uniswap_wrapper.get_token_eth_output_price(
                                            w33.toChecksumAddress(token7address),
                                            threeeth)
                                        token7eth2 = token7eth / threeeth
                                        if token7decimals != 18:
                                            pricetoken7usd = (priceeth['ethereum']['usd'] / (token7eth2)) / (
                                                    10 ** (18 - (token7decimals)))
                                        else:
                                            pricetoken7usd = (priceeth['ethereum']['usd'] / (token7eth2))
                                    dollarbalancetoken7 = pricetoken7usd * balance_token7
                                    if str(token8address) != '0':
                                        if priceright == 'sell':
                                            token8eth = uniswap_wrapper.get_eth_token_input_price(
                                                w33.toChecksumAddress(token8address),
                                                threeeth)
                                            token8eth2 = token8eth / threeeth
                                            if token8decimals != 18:
                                                pricetoken8usd = (priceeth['ethereum']['usd'] / (
                                                    token8eth2)) / (
                                                                         10 ** (18 - (token8decimals)))
                                            else:
                                                pricetoken8usd = (priceeth['ethereum']['usd'] / (token8eth2))
                                        else:
                                            token8eth = uniswap_wrapper.get_token_eth_output_price(
                                                w33.toChecksumAddress(token8address),
                                                threeeth)
                                            token8eth2 = token8eth / threeeth
                                            if token8decimals != 18:
                                                pricetoken8usd = (priceeth['ethereum']['usd'] / (
                                                    token8eth2)) / (
                                                                         10 ** (18 - (token8decimals)))
                                            else:
                                                pricetoken8usd = (priceeth['ethereum']['usd'] / (token8eth2))
                                        dollarbalancetoken8 = pricetoken8usd * balance_token8
                                        if str(token9address) != '0':
                                            if priceright == 'sell':
                                                token9eth = uniswap_wrapper.get_eth_token_input_price(
                                                    w33.toChecksumAddress(token9address),
                                                    threeeth)
                                                token9eth2 = token9eth / threeeth
                                                if token9decimals != 18:
                                                    pricetoken9usd = (priceeth['ethereum']['usd'] / (
                                                        token9eth2)) / (
                                                                             10 ** (18 - (token9decimals)))
                                                else:
                                                    pricetoken9usd = (
                                                            priceeth['ethereum']['usd'] / (token9eth2))
                                            else:
                                                token9eth = uniswap_wrapper.get_token_eth_output_price(
                                                    w33.toChecksumAddress(token9address),
                                                    threeeth)
                                                token9eth2 = token9eth / threeeth
                                                if token9decimals != 18:
                                                    pricetoken9usd = (priceeth['ethereum']['usd'] / (
                                                        token9eth2)) / (
                                                                             10 ** (18 - (token9decimals)))
                                                else:
                                                    pricetoken9usd = (
                                                            priceeth['ethereum']['usd'] / (token9eth2))
                                            dollarbalancetoken9 = pricetoken9usd * balance_token9
                                            if str(token10address) != '0':
                                                if priceright == 'sell':
                                                    token10eth = uniswap_wrapper.get_eth_token_input_price(
                                                        w33.toChecksumAddress(token10address),
                                                        threeeth)
                                                    token10eth2 = token10eth / threeeth
                                                    if token10decimals != 18:
                                                        pricetoken10usd = (priceeth['ethereum']['usd'] / (
                                                            token10eth2)) / (
                                                                                  10 ** (18 - (token10decimals)))
                                                    else:
                                                        pricetoken10usd = (
                                                                priceeth['ethereum']['usd'] / (token10eth2))
                                                else:
                                                    token10eth = uniswap_wrapper.get_token_eth_output_price(
                                                        w33.toChecksumAddress(token10address),
                                                        threeeth)
                                                    token10eth2 = token10eth / threeeth
                                                    if token10decimals != 18:
                                                        pricetoken10usd = (priceeth['ethereum']['usd'] / (
                                                            token10eth2)) / (
                                                                                  10 ** (18 - (token10decimals)))
                                                        dollarbalancetoken10 = pricetoken10usd * balance_token10
                                                    else:
                                                        pricetoken10usd = (
                                                                priceeth['ethereum']['usd'] / (token10eth2))
                                                        dollarbalancetoken10 = pricetoken10usd * balance_token10
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            if str(token1address) != '0':
                weergave1 = ('   [' + token1smallcasename + '  ' + str("{:.6f}".format(pricetoken1usd) + ']'))
            try:
                if str(token2address) != '0' and activatetoken2 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token2smallcasename + '  ' + str("{:.6f}".format(pricetoken2usd)) + ']')
                if str(token3address) != '0' and activatetoken3 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token3smallcasename + '  ' + str("{:.6f}".format(pricetoken3usd)) + ']')
                if str(token4address) != '0' and activatetoken4 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token4smallcasename + '  ' + str("{:.6f}".format(pricetoken4usd)) + ']')
                if str(token5address) != '0' and activatetoken5 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token5smallcasename + '  ' + str("{:.6f}".format(pricetoken5usd)) + ']')
                if str(token6address) != '0' and activatetoken6 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token6smallcasename + '  ' + str("{:.6f}".format(pricetoken6usd)) + ']')
                if str(token7address) != '0' and activatetoken7 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token7smallcasename + '  ' + str("{:.6f}".format(pricetoken7usd)) + ']')
                if str(token8address) != '0' and activatetoken8 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token8smallcasename + '  ' + str("{:.6f}".format(pricetoken8usd)) + ']')
                if str(token9address) != '0' and activatetoken9 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token9smallcasename + '  ' + str("{:.6f}".format(pricetoken9usd)) + ']')
                if str(token10address) != '0' and activatetoken10 == 1:
                    weergave1 = weergave1 + (
                            '    [' + token10smallcasename + '  ' + str("{:.6f}".format(pricetoken10usd)) + ']')
            except Exception as e:
                o = 0
            try:
                weergave = weergave1
                token1totoken2 = 0
                token1totoken3 = 0
                token1totoken4 = 0
                token1totoken5 = 0
                token1totoken6 = 0
                token1totoken7 = 0
                token1totoken8 = 0
                token1totoken9 = 0
                token1totoken10 = 0
                token2totoken1 = 0
                token2totoken3 = 0
                token2totoken4 = 0
                token2totoken5 = 0
                token2totoken6 = 0
                token2totoken7 = 0
                token2totoken8 = 0
                token2totoken9 = 0
                token2totoken10 = 0
                token3totoken2 = 0
                token3totoken1 = 0
                token3totoken4 = 0
                token3totoken5 = 0
                token3totoken6 = 0
                token3totoken7 = 0
                token3totoken8 = 0
                token3totoken9 = 0
                token3totoken10 = 0
                token4totoken2 = 0
                token4totoken3 = 0
                token4totoken1 = 0
                token4totoken5 = 0
                token4totoken6 = 0
                token4totoken7 = 0
                token4totoken8 = 0
                token4totoken9 = 0
                token4totoken10 = 0
                token5totoken2 = 0
                token5totoken3 = 0
                token5totoken4 = 0
                token5totoken1 = 0
                token5totoken6 = 0
                token5totoken7 = 0
                token5totoken8 = 0
                token5totoken9 = 0
                token5totoken10 = 0
                token6totoken2 = 0
                token6totoken3 = 0
                token6totoken4 = 0
                token6totoken5 = 0
                token6totoken1 = 0
                token6totoken7 = 0
                token6totoken8 = 0
                token6totoken9 = 0
                token6totoken10 = 0
                token7totoken2 = 0
                token7totoken3 = 0
                token7totoken4 = 0
                token7totoken5 = 0
                token7totoken6 = 0
                token7totoken1 = 0
                token7totoken8 = 0
                token7totoken9 = 0
                token7totoken10 = 0
                token8totoken2 = 0
                token8totoken3 = 0
                token8totoken4 = 0
                token8totoken5 = 0
                token8totoken6 = 0
                token8totoken7 = 0
                token8totoken1 = 0
                token8totoken9 = 0
                token8totoken10 = 0
                token9totoken2 = 0
                token9totoken3 = 0
                token9totoken4 = 0
                token9totoken5 = 0
                token9totoken6 = 0
                token9totoken7 = 0
                token9totoken8 = 0
                token9totoken1 = 0
                token9totoken10 = 0
                token10totoken2 = 0
                token10totoken3 = 0
                token10totoken4 = 0
                token10totoken5 = 0
                token10totoken6 = 0
                token10totoken7 = 0
                token10totoken8 = 0
                token10totoken9 = 0
                token10totoken1 = 0
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            if str(token2address) != '0':
                if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken1usd < (
                        (token1high + token1low) / 2):
                    token2totoken1 = ((pricetoken2usd - token2low) / (token2high - token2low)) / (
                            (pricetoken1usd - token1low) / (token1high - token1low))
                else:
                    token2totoken1 = 0.1

                if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken2usd < (
                        (token2high + token2low) / 2):
                    token1totoken2 = ((pricetoken1usd - token1low) / (token1high - token1low)) / (
                            (pricetoken2usd - token2low) / (token2high - token2low))
                else:
                    token1totoken2 = 0.1
                if str(token3address) != '0':
                    if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken3usd < (
                            (token3high + token3low) / 2):
                        token2totoken3 = ((pricetoken2usd - token2low) / (token2high - token2low)) / (
                                (pricetoken3usd - token3low) / (token3high - token3low))
                    else:
                        token2totoken3 = 0.1
                    if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken3usd < (
                            (token3high + token3low) / 2):
                        token1totoken3 = ((pricetoken1usd - token1low) / (token1high - token1low)) / (
                                (pricetoken3usd - token3low) / (token3high - token3low))
                    else:
                        token1totoken3 = 0.1
                    if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken2usd < (
                            (token2high + token2low) / 2):
                        token3totoken2 = ((pricetoken3usd - token3low) / (token3high - token3low)) / (
                                (pricetoken2usd - token2low) / (token2high - token2low))
                    else:
                        token3totoken2 = 0.1
                    if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken1usd < (
                            (token1high + token1low) / 2):
                        token3totoken1 = ((pricetoken3usd - token3low) / (token3high - token3low)) / (
                                (pricetoken1usd - token1low) / (token1high - token1low))
                    else:
                        token3totoken1 = 0.1
                    if str(token4address) != '0':
                        if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken4usd < (
                                (token4high + token4low) / 2):
                            token2totoken4 = ((pricetoken2usd - token2low) / (token2high - token2low)) / (
                                    (pricetoken4usd - token4low) / (token4high - token4low))
                        else:
                            token2totoken4 = 0.1
                        if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken4usd < (
                                (token4high + token4low) / 2):
                            token1totoken4 = ((pricetoken1usd - token1low) / (token1high - token1low)) / (
                                    (pricetoken4usd - token4low) / (token4high - token4low))
                        else:
                            token1totoken4 = 0.1
                        if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken2usd < (
                                (token2high + token2low) / 2):
                            token4totoken2 = ((pricetoken4usd - token4low) / (token4high - token4low)) / (
                                    (pricetoken2usd - token2low) / (token2high - token2low))
                        else:
                            token4totoken2 = 0.1
                        if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken1usd < (
                                (token1high + token1low) / 2):
                            token4totoken1 = ((pricetoken4usd - token4low) / (token4high - token4low)) / (
                                    (pricetoken1usd - token1low) / (token1high - token1low))
                        else:
                            token4totoken1 = 0.1
                        if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken3usd < (
                                (token3high + token3low) / 2):
                            token4totoken3 = ((pricetoken4usd - token4low) / (token4high - token4low)) / (
                                    (pricetoken3usd - token3low) / (token3high - token3low))
                        else:
                            token4totoken3 = 0.1
                        if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken4usd < (
                                (token4high + token4low) / 2):
                            token3totoken4 = ((pricetoken3usd - token3low) / (token3high - token3low)) / (
                                    (pricetoken4usd - token4low) / (token4high - token4low))
                        else:
                            token3totoken4 = 0.1
                        if str(token5address) != '0':
                            if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken5usd < (
                                    (token5high + token5low) / 2):
                                token2totoken5 = ((pricetoken2usd - token2low) / (token2high - token2low)) / (
                                        (pricetoken5usd - token5low) / (token5high - token5low))
                            else:
                                token2totoken5 = 0.1
                            if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken5usd < (
                                    (token5high + token5low) / 2):
                                token1totoken5 = ((pricetoken1usd - token1low) / (token1high - token1low)) / (
                                        (pricetoken5usd - token5low) / (token5high - token5low))
                            else:
                                token1totoken5 = 0.1
                            if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken2usd < (
                                    (token2high + token2low) / 2):
                                token5totoken2 = ((pricetoken5usd - token5low) / (token5high - token5low)) / (
                                        (pricetoken2usd - token2low) / (token2high - token2low))
                            else:
                                token5totoken2 = 0.1
                            if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken1usd < (
                                    (token1high + token1low) / 2):
                                token5totoken1 = ((pricetoken5usd - token5low) / (token5high - token5low)) / (
                                        (pricetoken1usd - token1low) / (token1high - token1low))
                            else:
                                token5totoken1 = 0.1
                            if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken3usd < (
                                    (token3high + token3low) / 2):
                                token5totoken3 = ((pricetoken5usd - token5low) / (token5high - token5low)) / (
                                        (pricetoken3usd - token3low) / (token3high - token3low))
                            else:
                                token5totoken3 = 0.1
                            if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken5usd < (
                                    (token5high + token5low) / 2):
                                token3totoken5 = ((pricetoken3usd - token3low) / (token3high - token3low)) / (
                                        (pricetoken5usd - token5low) / (token5high - token5low))
                            else:
                                token3totoken5 = 0.1
                            if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken4usd < (
                                    (token4high + token4low) / 2):
                                token5totoken4 = ((pricetoken5usd - token5low) / (token5high - token5low)) / (
                                        (pricetoken4usd - token4low) / (token4high - token4low))
                            else:
                                token5totoken4 = 0.1
                            if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken5usd < (
                                    (token5high + token5low) / 2):
                                token4totoken5 = ((pricetoken4usd - token4low) / (token4high - token4low)) / (
                                        (pricetoken5usd - token5low) / (token5high - token5low))
                            else:
                                token4totoken5 = 0.1
                            if str(token6address) != '0':
                                if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken6usd < (
                                        (token6high + token6low) / 2):
                                    token2totoken6 = ((pricetoken2usd - token2low) / (token2high - token2low)) / (
                                            (pricetoken6usd - token6low) / (token6high - token6low))
                                else:
                                    token2totoken6 = 0.1
                                if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken6usd < (
                                        (token6high + token6low) / 2):
                                    token1totoken6 = ((pricetoken1usd - token1low) / (token1high - token1low)) / (
                                            (pricetoken6usd - token6low) / (token6high - token6low))
                                else:
                                    token1totoken6 = 0.1
                                if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken2usd < (
                                        (token2high + token2low) / 2):
                                    token6totoken2 = ((pricetoken6usd - token6low) / (token6high - token6low)) / (
                                            (pricetoken2usd - token2low) / (token2high - token2low))
                                else:
                                    token6totoken2 = 0.1
                                if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken1usd < (
                                        (token1high + token1low) / 2):
                                    token6totoken1 = ((pricetoken6usd - token6low) / (token6high - token6low)) / (
                                            (pricetoken1usd - token1low) / (token1high - token1low))
                                else:
                                    token6totoken1 = 0.1
                                if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken3usd < (
                                        (token3high + token3low) / 2):
                                    token6totoken3 = ((pricetoken6usd - token6low) / (token6high - token6low)) / (
                                            (pricetoken3usd - token3low) / (token3high - token3low))
                                else:
                                    token6totoken3 = 0.1
                                if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken6usd < (
                                        (token6high + token6low) / 2):
                                    token3totoken6 = ((pricetoken3usd - token3low) / (token3high - token3low)) / (
                                            (pricetoken6usd - token6low) / (token6high - token6low))
                                else:
                                    token3totoken6 = 0.1
                                if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken4usd < (
                                        (token4high + token4low) / 2):
                                    token6totoken4 = ((pricetoken6usd - token6low) / (token6high - token6low)) / (
                                            (pricetoken4usd - token4low) / (token4high - token4low))
                                else:
                                    token6totoken4 = 0.1
                                if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken6usd < (
                                        (token6high + token6low) / 2):
                                    token4totoken6 = ((pricetoken4usd - token4low) / (token4high - token4low)) / (
                                            (pricetoken6usd - token6low) / (token6high - token6low))
                                else:
                                    token4totoken6 = 0.1
                                if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken5usd < (
                                        (token5high + token5low) / 2):
                                    token6totoken5 = ((pricetoken6usd - token6low) / (token6high - token6low)) / (
                                            (pricetoken5usd - token5low) / (token5high - token5low))
                                else:
                                    token6totoken5 = 0.1
                                if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken6usd < (
                                        (token6high + token6low) / 2):
                                    token5totoken6 = ((pricetoken5usd - token5low) / (token5high - token5low)) / (
                                            (pricetoken6usd - token6low) / (token6high - token6low))
                                else:
                                    token5totoken6 = 0.1
                                if str(token7address) != '0':
                                    if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token2totoken7 = ((pricetoken2usd - token2low) / (
                                                token2high - token2low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token2totoken7 = 0.1
                                    if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token1totoken7 = ((pricetoken1usd - token1low) / (
                                                token1high - token1low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token1totoken7 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken2usd < (
                                            (token2high + token2low) / 2):
                                        token7totoken2 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken2usd - token2low) / (
                                                                 token2high - token2low))
                                    else:
                                        token7totoken2 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken1usd < (
                                            (token1high + token1low) / 2):
                                        token7totoken1 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken1usd - token1low) / (
                                                                 token1high - token1low))
                                    else:
                                        token7totoken1 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken3usd < (
                                            (token3high + token3low) / 2):
                                        token7totoken3 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken3usd - token3low) / (
                                                                 token3high - token3low))
                                    else:
                                        token7totoken3 = 0.1
                                    if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token3totoken7 = ((pricetoken3usd - token3low) / (
                                                token3high - token3low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token3totoken7 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken4usd < (
                                            (token4high + token4low) / 2):
                                        token7totoken4 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken4usd - token4low) / (
                                                                 token4high - token4low))
                                    else:
                                        token7totoken4 = 0.1
                                    if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token4totoken7 = ((pricetoken4usd - token4low) / (
                                                token4high - token4low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token4totoken7 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken5usd < (
                                            (token5high + token5low) / 2):
                                        token7totoken5 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken5usd - token5low) / (
                                                                 token5high - token5low))
                                    else:
                                        token7totoken5 = 0.1
                                    if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token5totoken7 = ((pricetoken5usd - token5low) / (
                                                token5high - token5low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token5totoken7 = 0.1
                                    if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken6usd < (
                                            (token6high + token6low) / 2):
                                        token7totoken6 = ((pricetoken7usd - token7low) / (
                                                token7high - token7low)) / (
                                                                 (pricetoken6usd - token6low) / (
                                                                 token6high - token6low))
                                    else:
                                        token7totoken6 = 0.1
                                    if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken7usd < (
                                            (token7high + token7low) / 2):
                                        token6totoken7 = ((pricetoken6usd - token6low) / (
                                                token6high - token6low)) / (
                                                                 (pricetoken7usd - token7low) / (
                                                                 token7high - token7low))
                                    else:
                                        token6totoken7 = 0.1
                                    if str(token8address) != '0':
                                        if pricetoken2usd > ((token2high + token2low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token2totoken8 = ((pricetoken2usd - token2low) / (
                                                    token2high - token2low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token2totoken8 = 0.1
                                        if pricetoken1usd > ((token1high + token1low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token1totoken8 = ((pricetoken1usd - token1low) / (
                                                    token1high - token1low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token1totoken8 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken2usd < (
                                                (token2high + token2low) / 2):
                                            token8totoken2 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken2usd - token2low) / (
                                                                     token2high - token2low))
                                        else:
                                            token8totoken2 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken1usd < (
                                                (token1high + token1low) / 2):
                                            token8totoken1 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken1usd - token1low) / (
                                                                     token1high - token1low))
                                        else:
                                            token8totoken1 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken3usd < (
                                                (token3high + token3low) / 2):
                                            token8totoken3 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken3usd - token3low) / (
                                                                     token3high - token3low))
                                        else:
                                            token8totoken3 = 0.1
                                        if pricetoken3usd > ((token3high + token3low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token3totoken8 = ((pricetoken3usd - token3low) / (
                                                    token3high - token3low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token3totoken8 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken4usd < (
                                                (token4high + token4low) / 2):
                                            token8totoken4 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken4usd - token4low) / (
                                                                     token4high - token4low))
                                        else:
                                            token8totoken4 = 0.1
                                        if pricetoken4usd > ((token4high + token4low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token4totoken8 = ((pricetoken4usd - token4low) / (
                                                    token4high - token4low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token4totoken8 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken5usd < (
                                                (token5high + token5low) / 2):
                                            token8totoken5 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken5usd - token5low) / (
                                                                     token5high - token5low))
                                        else:
                                            token8totoken5 = 0.1
                                        if pricetoken5usd > ((token5high + token5low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token5totoken8 = ((pricetoken5usd - token5low) / (
                                                    token5high - token5low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token5totoken8 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken6usd < (
                                                (token6high + token6low) / 2):
                                            token8totoken6 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken6usd - token6low) / (
                                                                     token6high - token6low))
                                        else:
                                            token8totoken6 = 0.1
                                        if pricetoken6usd > ((token6high + token6low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token6totoken8 = ((pricetoken6usd - token6low) / (
                                                    token6high - token6low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token6totoken8 = 0.1
                                        if pricetoken8usd > ((token8high + token8low) / 2) and pricetoken7usd < (
                                                (token7high + token7low) / 2):
                                            token8totoken7 = ((pricetoken8usd - token8low) / (
                                                    token8high - token8low)) / (
                                                                     (pricetoken7usd - token7low) / (
                                                                     token7high - token7low))
                                        else:
                                            token8totoken7 = 0.1
                                        if pricetoken7usd > ((token7high + token7low) / 2) and pricetoken8usd < (
                                                (token8high + token8low) / 2):
                                            token7totoken8 = ((pricetoken7usd - token7low) / (
                                                    token7high - token7low)) / (
                                                                     (pricetoken8usd - token8low) / (
                                                                     token8high - token8low))
                                        else:
                                            token7totoken8 = 0.1
                                        if str(token9address) != '0':
                                            if pricetoken2usd > (
                                                    (token2high + token2low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token2totoken9 = ((pricetoken2usd - token2low) / (
                                                        token2high - token2low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token2totoken9 = 0.1
                                            if pricetoken1usd > (
                                                    (token1high + token1low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token1totoken9 = ((pricetoken1usd - token1low) / (
                                                        token1high - token1low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token1totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken2usd < (
                                                    (token2high + token2low) / 2):
                                                token9totoken2 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken2usd - token2low) / (
                                                                         token2high - token2low))
                                            else:
                                                token9totoken2 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken1usd < (
                                                    (token1high + token1low) / 2):
                                                token9totoken1 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken1usd - token1low) / (
                                                                         token1high - token1low))
                                            else:
                                                token9totoken1 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken3usd < (
                                                    (token3high + token3low) / 2):
                                                token9totoken3 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken3usd - token3low) / (
                                                                         token3high - token3low))
                                            else:
                                                token9totoken3 = 0.1
                                            if pricetoken3usd > (
                                                    (token3high + token3low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token3totoken9 = ((pricetoken3usd - token3low) / (
                                                        token3high - token3low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token3totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken4usd < (
                                                    (token4high + token4low) / 2):
                                                token9totoken4 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken4usd - token4low) / (
                                                                         token4high - token4low))
                                            else:
                                                token9totoken4 = 0.1
                                            if pricetoken4usd > (
                                                    (token4high + token4low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token4totoken9 = ((pricetoken4usd - token4low) / (
                                                        token4high - token4low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token4totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken5usd < (
                                                    (token5high + token5low) / 2):
                                                token9totoken5 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken5usd - token5low) / (
                                                                         token5high - token5low))
                                            else:
                                                token9totoken5 = 0.1
                                            if pricetoken5usd > (
                                                    (token5high + token5low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token5totoken9 = ((pricetoken5usd - token5low) / (
                                                        token5high - token5low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token5totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken6usd < (
                                                    (token6high + token6low) / 2):
                                                token9totoken6 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken6usd - token6low) / (
                                                                         token6high - token6low))
                                            else:
                                                token9totoken6 = 0.1
                                            if pricetoken6usd > (
                                                    (token6high + token6low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token6totoken9 = ((pricetoken6usd - token6low) / (
                                                        token6high - token6low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token6totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken7usd < (
                                                    (token7high + token7low) / 2):
                                                token9totoken7 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken7usd - token7low) / (
                                                                         token7high - token7low))
                                            else:
                                                token9totoken7 = 0.1
                                            if pricetoken7usd > (
                                                    (token7high + token7low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token7totoken9 = ((pricetoken7usd - token7low) / (
                                                        token7high - token7low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token7totoken9 = 0.1
                                            if pricetoken9usd > (
                                                    (token9high + token9low) / 2) and pricetoken8usd < (
                                                    (token8high + token8low) / 2):
                                                token9totoken8 = ((pricetoken9usd - token9low) / (
                                                        token9high - token9low)) / (
                                                                         (pricetoken8usd - token8low) / (
                                                                         token8high - token8low))
                                            else:
                                                token9totoken8 = 0.1
                                            if pricetoken8usd > (
                                                    (token8high + token8low) / 2) and pricetoken9usd < (
                                                    (token9high + token9low) / 2):
                                                token8totoken9 = ((pricetoken8usd - token8low) / (
                                                        token8high - token8low)) / (
                                                                         (pricetoken9usd - token9low) / (
                                                                         token9high - token9low))
                                            else:
                                                token8totoken9 = 0.1
                                            if str(token10address) != '0':
                                                if pricetoken2usd > (
                                                        (token2high + token2low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token2totoken10 = ((pricetoken2usd - token2low) / (
                                                            token2high - token2low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token2totoken10 = 0.1
                                                if pricetoken1usd > (
                                                        (token1high + token1low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token1totoken10 = ((pricetoken1usd - token1low) / (
                                                            token1high - token1low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token1totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken2usd < (
                                                        (token2high + token2low) / 2):
                                                    token10totoken2 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken2usd - token2low) / (
                                                                              token2high - token2low))
                                                else:
                                                    token10totoken2 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken1usd < (
                                                        (token1high + token1low) / 2):
                                                    token10totoken1 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken1usd - token1low) / (
                                                                              token1high - token1low))
                                                else:
                                                    token10totoken1 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken3usd < (
                                                        (token3high + token3low) / 2):
                                                    token10totoken3 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken3usd - token3low) / (
                                                                              token3high - token3low))
                                                else:
                                                    token10totoken3 = 0.1
                                                if pricetoken3usd > (
                                                        (token3high + token3low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token3totoken10 = ((pricetoken3usd - token3low) / (
                                                            token3high - token3low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token3totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken4usd < (
                                                        (token4high + token4low) / 2):
                                                    token10totoken4 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken4usd - token4low) / (
                                                                              token4high - token4low))
                                                else:
                                                    token10totoken4 = 0.1
                                                if pricetoken4usd > (
                                                        (token4high + token4low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token4totoken10 = ((pricetoken4usd - token4low) / (
                                                            token4high - token4low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token4totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken5usd < (
                                                        (token5high + token5low) / 2):
                                                    token10totoken5 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken5usd - token5low) / (
                                                                              token5high - token5low))
                                                else:
                                                    token10totoken5 = 0.1
                                                if pricetoken5usd > (
                                                        (token5high + token5low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token5totoken10 = ((pricetoken5usd - token5low) / (
                                                            token5high - token5low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token5totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken6usd < (
                                                        (token6high + token6low) / 2):
                                                    token10totoken6 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken6usd - token6low) / (
                                                                              token6high - token6low))
                                                else:
                                                    token10totoken6 = 0.1
                                                if pricetoken6usd > (
                                                        (token6high + token6low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token6totoken10 = ((pricetoken6usd - token6low) / (
                                                            token6high - token6low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token6totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken7usd < (
                                                        (token7high + token7low) / 2):
                                                    token10totoken7 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken7usd - token7low) / (
                                                                              token7high - token7low))
                                                else:
                                                    token10totoken7 = 0.1
                                                if pricetoken7usd > (
                                                        (token7high + token7low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token7totoken10 = ((pricetoken7usd - token7low) / (
                                                            token7high - token7low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token7totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken8usd < (
                                                        (token8high + token8low) / 2):
                                                    token10totoken8 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken8usd - token8low) / (
                                                                              token8high - token8low))
                                                else:
                                                    token10totoken8 = 0.1
                                                if pricetoken8usd > (
                                                        (token8high + token8low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token8totoken10 = ((pricetoken8usd - token8low) / (
                                                            token8high - token8low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token8totoken10 = 0.1
                                                if pricetoken10usd > (
                                                        (token10high + token10low) / 2) and pricetoken9usd < (
                                                        (token9high + token9low) / 2):
                                                    token10totoken9 = ((pricetoken10usd - token10low) / (
                                                            token10high - token10low)) / (
                                                                              (pricetoken9usd - token9low) / (
                                                                              token9high - token9low))
                                                else:
                                                    token10totoken9 = 0.1
                                                if pricetoken9usd > (
                                                        (token9high + token9low) / 2) and pricetoken10usd < (
                                                        (token10high + token10low) / 2):
                                                    token9totoken10 = ((pricetoken9usd - token9low) / (
                                                            token9high - token9low)) / (
                                                                              (pricetoken10usd - token10low) / (
                                                                              token10high - token10low))
                                                else:
                                                    token9totoken10 = 0.1
            notyet = 3
            return {'priceeth': priceeth, 'pricetoken1usd': pricetoken1usd, 'pricetoken2usd': pricetoken2usd,
                        'token1totoken2': token1totoken2, 'token2totoken1': token2totoken1,
                        'pricetoken3usd': pricetoken3usd,
                        'pricetoken4usd': pricetoken4usd, 'pricetoken5usd': pricetoken5usd,
                        'pricetoken6usd': pricetoken6usd,
                        'pricetoken7usd': pricetoken7usd, 'pricetoken8usd': pricetoken8usd,
                        'pricetoken9usd': pricetoken9usd,
                        'pricetoken10usd': pricetoken10usd, 'token1totoken7': token1totoken7,
                        'token1totoken8': token1totoken8,
                        'token1totoken9': token1totoken9, 'token1totoken3': token1totoken3,
                        'token1totoken4': token1totoken4,
                        'token1totoken5': token1totoken5, 'token1totoken6': token1totoken6,
                        'token1totoken10': token1totoken10,
                        'token2totoken3': token2totoken3, 'token2totoken4': token2totoken4,
                        'token2totoken5': token2totoken5,
                        'token2totoken6': token2totoken6, 'token2totoken7': token2totoken7,
                        'token2totoken8': token2totoken8,
                        'token2totoken9': token2totoken9, 'token2totoken10': token2totoken10,
                        'token3totoken1': token3totoken1,
                        'token3totoken2': token3totoken2, 'token3totoken4': token3totoken4,
                        'token3totoken5': token3totoken5,
                        'token3totoken6': token3totoken6, 'token3totoken7': token3totoken7,
                        'token3totoken8': token3totoken8,
                        'token3totoken9': token3totoken9, 'token3totoken10': token3totoken10,
                        'token4totoken1': token4totoken1,
                        'token4totoken2': token4totoken2, 'token4totoken3': token4totoken3,
                        'token4totoken5': token4totoken5,
                        'token4totoken6': token4totoken6, 'token4totoken7': token4totoken7,
                        'token4totoken8': token4totoken8,
                        'token4totoken9': token4totoken9, 'token4totoken10': token4totoken10,
                        'token5totoken1': token5totoken1,
                        'token5totoken2': token5totoken2, 'token5totoken4': token5totoken4,
                        'token5totoken3': token5totoken3,
                        'token5totoken6': token5totoken6, 'token5totoken7': token5totoken7,
                        'token5totoken8': token5totoken8,
                        'token5totoken9': token5totoken9, 'token5totoken10': token5totoken10,
                        'token6totoken1': token6totoken1,
                        'token6totoken2': token6totoken2, 'token6totoken4': token6totoken4,
                        'token6totoken5': token6totoken5,
                        'token6totoken3': token6totoken3, 'token6totoken7': token6totoken7,
                        'token6totoken8': token6totoken8,
                        'token6totoken9': token6totoken9, 'token6totoken10': token6totoken10,
                        'token7totoken1': token7totoken1,
                        'token7totoken2': token7totoken2, 'token7totoken4': token7totoken4,
                        'token7totoken5': token7totoken5,
                        'token7totoken6': token7totoken6, 'token7totoken3': token7totoken3,
                        'token7totoken8': token7totoken8,
                        'token7totoken9': token7totoken9, 'token7totoken10': token7totoken10,
                        'token8totoken1': token8totoken1,
                        'token8totoken2': token8totoken2, 'token8totoken4': token8totoken4,
                        'token8totoken5': token8totoken5,
                        'token8totoken6': token8totoken6, 'token8totoken7': token8totoken7,
                        'token8totoken3': token8totoken3,
                        'token8totoken9': token8totoken9, 'token8totoken10': token8totoken10,
                        'token9totoken1': token9totoken1,
                        'token9totoken2': token9totoken2, 'token9totoken4': token9totoken4,
                        'token9totoken5': token9totoken5,
                        'token9totoken6': token9totoken6, 'token9totoken7': token9totoken7,
                        'token9totoken8': token9totoken8,
                        'token9totoken3': token9totoken3, 'token9totoken10': token9totoken10,
                        'token10totoken1': token10totoken1,
                        'token10totoken2': token10totoken2, 'token10totoken4': token10totoken4,
                        'token10totoken5': token10totoken5,
                        'token10totoken6': token10totoken6, 'token10totoken7': token10totoken7,
                        'token10totoken8': token10totoken8,
                        'token10totoken9': token10totoken9, 'token10totoken3': token10totoken3, 'weergave': weergave,
                        'notyet': notyet, 'dollarbalancetoken1': dollarbalancetoken1, 'dollarbalancetoken2': dollarbalancetoken2, 'dollarbalancetoken3': dollarbalancetoken3, 'dollarbalancetoken4': dollarbalancetoken4, 'dollarbalancetoken5': dollarbalancetoken5,'dollarbalancetoken6': dollarbalancetoken6, 'dollarbalancetoken7': dollarbalancetoken7,'dollarbalancetoken8': dollarbalancetoken8,'dollarbalancetoken9': dollarbalancetoken9, 'dollarbalancetoken10': dollarbalancetoken10,'dollarbalancemaintoken': dollarbalancemaintoken}

        if 'step' not in globals():
            step=1
        else:
            step=step+1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()
        if self.__abort==True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
        #def marketordersell():
            #def marketorderbuy():

                #def preapproval():

                #def recharge():


        # paytokenholding
        if 0 == 1:
            details2 = {'symbol': paytokensmallname, 'address': paytokenaddress,
                        'decimals': paytokendecimals,
                        'name': paytokenname}
            erc20tokens2 = ethbalance.add_token(token2, details2)
            ethamount2 = math.floor(ethbalance.get_token_balance(paytokenname, my_address)['balance'])
            if ethamount2 < paytokenamount:
                print("You are not holding the required token, the application will now stop")
                exit()
                subprocess.call(["taskkill", "/F", "/IM", "bot.exe"])
                time.sleep(4294960)
        if 'step' not in globals():
            step=1
        else:
            step=step+1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()

        if self.__abort==True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
        while self.__abort != True:
            try:
                w33 = Web3()
                try:
                    def api(speed):
                        res = requests.get(
                            'https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key=f2ff6e6755c2123799676dbe8ed3af94574000b4c9b56d1f159510ec91b0')
                        data = (res.json()[speed]) / 10
                        return data

                    gwei = api(speed)
                    print('Gwei for ' + str(speed) + ' trading at the moment: ' + str(gwei))

                except Exception as e:
                    o = 0
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    #w33.eth.setGasPriceStrategy(fast_gas_price_strategy)
                w33.middleware_onion.add(middleware.time_based_cache_middleware)
                w33.middleware_onion.add(middleware.latest_block_based_cache_middleware)
                w33.middleware_onion.add(middleware.simple_cache_middleware)
                w3 = Web3(Web3.HTTPProvider(infura_url))

                if token1ethaddress == '0':
                    print(
                        'Please stop the application and add at least token1, otherwise the application will do nothing. Don\'t worry, adding a token and activating it will only price check, and not trade :)')
                address = my_address
                private_key = my_pk
                uniswap_wrapper = Uniswap(address, private_key, web3=w3, version=2)
                ethereum_address = address
                if 'gelukt' not in globals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                    if 'step' not in globals():
                        step = 1
                    else:
                        step = step + 1
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()

                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        break
                    rara = checkbalance(infura_url, my_address, token1address, token2address, token3address,
                                        token4address,
                                        token5address,
                                        token6address, token7address, token8address, token9address, token10address,
                                        maincoinoption, token1decimals, token2decimals, token3decimals, token4decimals,
                                        token5decimals, token6decimals, token7decimals, token8decimals, token9decimals,
                                        token10decimals)

                    gelukt = rara['gelukt']
                    gelukt2 = rara['gelukt2']
                    keer = rara['keer']
                    balance_token1 = rara['balance_token1']
                    balance_token2 = rara['balance_token2']
                    balance_token3 = rara['balance_token3']
                    balance_token4 = rara['balance_token4']
                    balance_token5 = rara['balance_token5']
                    balance_token6 = rara['balance_token6']
                    balance_token7 = rara['balance_token7']
                    balance_token8 = rara['balance_token8']
                    balance_token9 = rara['balance_token9']
                    balance_token10 = rara['balance_token10']
                    maintokenbalance = rara['maintokenbalance']
                    print('Last thing we did is ' + gelukt + '. Second token available for trading is ' + gelukt2)
                if 'step' not in globals():
                    step = 1
                else:
                    step = step + 1
                while self.__abort != True:

                    # check if we need to abort the loop; need to process events to receive signals;
                    self.sig_step.emit(self.__id, 'step ' + str(step))
                    QCoreApplication.processEvents()
                    if self.__abort == True:
                        # note that "step" value will not necessarily be same for every thread
                        self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                        break
                    keer = keer + 1
                    if keer > 300 or 'gelukt' not in globals() or gelukt == "mislukt" or gelukt == "mislukt buy" or gelukt == "mislukt sell":
                        rara = checkbalance(infura_url, my_address, token1address, token2address, token3address,
                                            token4address,
                                            token5address,
                                            token6address, token7address, token8address, token9address, token10address,
                                            maincoinoption, token1decimals, token2decimals, token3decimals,
                                            token4decimals, token5decimals, token6decimals, token7decimals,
                                            token8decimals, token9decimals, token10decimals)
                        gelukt = rara['gelukt']
                        gelukt2 = rara['gelukt2']
                        keer = rara['keer']
                        balance_token1 = rara['balance_token1']
                        balance_token2 = rara['balance_token2']
                        balance_token3 = rara['balance_token3']
                        balance_token4 = rara['balance_token4']
                        balance_token5 = rara['balance_token5']
                        balance_token6 = rara['balance_token6']
                        balance_token7 = rara['balance_token7']
                        balance_token8 = rara['balance_token8']
                        balance_token9 = rara['balance_token9']
                        balance_token10 = rara['balance_token10']
                        maintokenbalance = rara['maintokenbalance']

                    try:
                        if "weergave" in locals():
                            weergave1 = weergave
                        if 'step' not in globals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            break
                        ku = getprice(token1address=token1address, token1smallcasename=token1smallcasename,
                                      token2address=token2address, token2smallcasename=token2smallcasename,
                                      token3address=token3address,
                                      token3smallcasename=token3smallcasename, token4address=token4address,
                                      token4smallcasename=token4smallcasename, token5address=token5address,
                                      token5smallcasename=token5smallcasename, token6address=token6address,
                                      token6smallcasename=token6smallcasename,
                                      token7address=token7address, token7smallcasename=token7smallcasename,
                                      token8address=token8address, token8smallcasename=token8smallcasename,
                                      token9address=token9address,
                                      token9smallcasename=token9smallcasename,
                                      token10address=token10address, token10smallcasename=token10smallcasename,
                                      token1high=token1high, token1low=token1low, token2high=token2high,
                                      token2low=token2low,
                                      token3high=token3high,
                                      token3low=token3low,
                                      token4high=token4high, token4low=token4low, token5high=token5high,
                                      token5low=token5low,
                                      token6high=token6high, token6low=token6low, token7high=token7high,
                                      token7low=token7low,
                                      token8high=token8high,
                                      token8low=token8low, token9high=token9high, token9low=token9low,
                                      token10high=token10high,
                                      token10low=token10low, incaseofbuyinghowmuch=incaseofbuyinghowmuch,
                                      uniswap_wrapper=Uniswap(address, private_key, web3=w3, version=2),
                                      timesleep=timesleep, gelukt=gelukt, token1decimals=token1decimals,
                                      token2decimals=token2decimals,
                                      token3decimals=token3decimals, token4decimals=token4decimals,
                                      token5decimals=token5decimals,
                                      token6decimals=token6decimals, token7decimals=token7decimals,
                                      token8decimals=token8decimals,
                                      token9decimals=token9decimals, token10decimals=token10decimals,
                                      activatetoken1=activatetoken1, activatetoken2=activatetoken2,
                                      activatetoken3=activatetoken3, activatetoken4=activatetoken4,
                                      activatetoken5=activatetoken5, activatetoken6=activatetoken6,
                                      activatetoken7=activatetoken7, activatetoken8=activatetoken8,
                                      activatetoken9=activatetoken9, activatetoken10=activatetoken10,
                                      balance_token1=balance_token1,
                                      balance_token2=balance_token2, balance_token3=balance_token3,
                                      balance_token4=balance_token4,
                                      balance_token5=balance_token5, balance_token6=balance_token6,
                                      balance_token7=balance_token7,
                                      balance_token8=balance_token8, balance_token9=balance_token9,
                                      balance_token10=balance_token10,
                                      maintokenbalance=maintokenbalance, ethaddress=maincoinoption, maindecimals=maindecimals)
                        dollarbalancetoken1 = ku['dollarbalancetoken1']
                        dollarbalancetoken2 = ku['dollarbalancetoken2']
                        dollarbalancetoken3 = ku['dollarbalancetoken3']
                        dollarbalancetoken4 = ku['dollarbalancetoken4']
                        dollarbalancetoken5 = ku['dollarbalancetoken5']
                        dollarbalancetoken6 = ku['dollarbalancetoken6']
                        dollarbalancetoken7 = ku['dollarbalancetoken7']
                        dollarbalancetoken8 = ku['dollarbalancetoken8']
                        dollarbalancetoken9 = ku['dollarbalancetoken9']
                        dollarbalancetoken10 = ku['dollarbalancetoken10']
                        dollarbalancemaintoken = ku['dollarbalancemaintoken']
                        totaldollars = dollarbalancetoken1 + dollarbalancetoken2 + dollarbalancetoken3 + dollarbalancetoken4 + dollarbalancetoken5 + dollarbalancetoken6 + dollarbalancetoken7 + dollarbalancetoken8 + dollarbalancetoken9 + dollarbalancetoken10 + dollarbalancemaintoken
                        weergavegeld=str(token1smallcasename)+':$'+str(dollarbalancetoken1)
                        if dollarbalancetoken2!=0:
                            weergavegeld=weergavegeld+'   '+str(token2smallcasename)+':$'+str(dollarbalancetoken2)
                            if dollarbalancetoken3 != 0:
                                weergavegeld = weergavegeld + '   ' + str(token3smallcasename) + ':$' + str(
                                    dollarbalancetoken3)
                                if dollarbalancetoken4 != 0:
                                    weergavegeld = weergavegeld + '   ' + str(token4smallcasename) + ':$' + str(
                                        dollarbalancetoken4)
                                    if dollarbalancetoken5 != 0:
                                        weergavegeld = weergavegeld + '   ' + str(token5smallcasename) + ':$' + str(
                                            dollarbalancetoken5)
                                        if dollarbalancetoken6 != 0:
                                            weergavegeld = weergavegeld + '   ' + str(token6smallcasename) + ':$' + str(
                                                dollarbalancetoken6)
                                            if dollarbalancetoken7 != 0:
                                                weergavegeld = weergavegeld + '   ' + str(
                                                    token7smallcasename) + ':$' + str(dollarbalancetoken7)
                                                if dollarbalancetoken8 != 0:
                                                    weergavegeld = weergavegeld + '   ' + str(
                                                        token8smallcasename) + ':$' + str(dollarbalancetoken8)
                                                    if dollarbalancetoken9 != 0:
                                                        weergavegeld = weergavegeld + '   ' + str(
                                                            token9smallcasename) + ':$' + str(dollarbalancetoken9)
                                                        if dollarbalancetoken10 != 0:
                                                            weergavegeld = weergavegeld + '   ' + str(
                                                                token10smallcasename) + ':$' + str(dollarbalancetoken10)
                        if 'nogeenkeer' not in locals():
                            nogeenkeer=1
                            print('Current balance:  '+weergavegeld)
                        else:
                            nogeenkeer=nogeenkeer+1
                            if nogeenkeer > 300:
                                print('Current balance:  ' + weergavegeld)
                                nogeenkeer=1
                        if 'step' not in globals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()
                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            break

                        try:
                            weergave12 = ku['weergave']
                            weergave = weergave12
                            notyet = ku['notyet']
                            priceeth = ku['priceeth']
                            pricetoken1usd = ku['pricetoken1usd']
                            pricetoken2usd = ku['pricetoken2usd']

                            token1totoken2 = ku['token1totoken2']
                            token2totoken1 = ku['token2totoken1']
                            pricetoken3usd = ku['pricetoken3usd']

                            pricetoken4usd = ku['pricetoken4usd']
                            pricetoken5usd = ku['pricetoken5usd']
                            pricetoken6usd = ku['pricetoken6usd']

                            pricetoken7usd = ku['pricetoken7usd']
                            pricetoken8usd = ku['pricetoken8usd']
                            pricetoken9usd = ku['pricetoken9usd']

                            pricetoken10usd = ku['pricetoken10usd']
                            token1totoken7 = ku['token1totoken7']
                            token1totoken8 = ku['token1totoken8']
                            token1totoken9 = ku['token1totoken9']

                            token1totoken3 = ku['token1totoken3']
                            token1totoken4 = ku['token1totoken4']
                            token1totoken5 = ku['token1totoken5']
                            token1totoken6 = ku['token1totoken6']

                            token1totoken10 = ku['token1totoken10']
                            token2totoken3 = ku['token2totoken3']
                            token2totoken4 = ku['token2totoken4']
                            token2totoken5 = ku['token2totoken5']

                            token2totoken6 = ku['token2totoken6']
                            token2totoken7 = ku['token2totoken7']
                            token2totoken8 = ku['token2totoken8']
                            token2totoken9 = ku['token2totoken9']

                            token2totoken10 = ku['token2totoken10']

                            token3totoken1 = ku['token3totoken1']
                            token3totoken2 = ku['token3totoken2']
                            token3totoken4 = ku['token3totoken4']

                            token3totoken5 = ku['token3totoken5']
                            token3totoken6 = ku['token3totoken6']
                            token3totoken7 = ku['token3totoken7']
                            token3totoken8 = ku['token3totoken8']

                            token3totoken9 = ku['token3totoken9']
                            token3totoken10 = ku['token3totoken10']

                            token4totoken1 = ku['token4totoken1']
                            token4totoken2 = ku['token4totoken2']
                            token4totoken3 = ku['token4totoken3']

                            token4totoken5 = ku['token4totoken5']
                            token4totoken6 = ku['token4totoken6']
                            token4totoken7 = ku['token4totoken7']
                            token4totoken8 = ku['token4totoken8']

                            token4totoken9 = ku['token4totoken9']
                            token4totoken10 = ku['token4totoken10']

                            token5totoken1 = ku['token5totoken1']
                            token5totoken2 = ku['token5totoken2']
                            token5totoken4 = ku['token5totoken4']

                            token5totoken3 = ku['token5totoken3']
                            token5totoken6 = ku['token5totoken6']
                            token5totoken7 = ku['token5totoken7']

                            token5totoken8 = ku['token5totoken8']

                            token5totoken9 = ku['token5totoken9']
                            token5totoken10 = ku['token5totoken10']

                            token6totoken1 = ku['token6totoken1']
                            token6totoken2 = ku['token6totoken2']
                            token6totoken4 = ku['token6totoken4']

                            token6totoken5 = ku['token6totoken5']
                            token6totoken3 = ku['token6totoken3']
                            token6totoken7 = ku['token6totoken7']

                            token6totoken8 = ku['token6totoken8']

                            token6totoken9 = ku['token6totoken9']
                            token6totoken10 = ku['token6totoken10']

                            token7totoken1 = ku['token7totoken1']
                            token7totoken2 = ku['token7totoken2']
                            token7totoken4 = ku['token7totoken4']

                            token7totoken5 = ku['token7totoken5']
                            token7totoken6 = ku['token7totoken6']
                            token7totoken3 = ku['token7totoken3']

                            token7totoken8 = ku['token7totoken8']

                            token7totoken9 = ku['token7totoken9']
                            token7totoken10 = ku['token7totoken10']

                            token8totoken1 = ku['token8totoken1']
                            token8totoken2 = ku['token8totoken2']
                            token8totoken4 = ku['token8totoken4']

                            token8totoken5 = ku['token8totoken5']
                            token8totoken6 = ku['token8totoken6']
                            token8totoken7 = ku['token8totoken7']

                            token8totoken3 = ku['token8totoken3']

                            token8totoken9 = ku['token8totoken9']
                            token8totoken10 = ku['token8totoken10']

                            token9totoken1 = ku['token9totoken1']
                            token9totoken2 = ku['token9totoken2']
                            token9totoken4 = ku['token9totoken4']

                            token9totoken5 = ku['token9totoken5']
                            token9totoken6 = ku['token9totoken6']
                            token9totoken7 = ku['token9totoken7']

                            token9totoken8 = ku['token9totoken8']

                            token9totoken3 = ku['token9totoken3']
                            token9totoken10 = ku['token9totoken10']

                            token10totoken1 = ku['token10totoken1']
                            token10totoken2 = ku['token10totoken2']
                            token10totoken4 = ku['token10totoken4']

                            token10totoken5 = ku['token10totoken5']
                            token10totoken6 = ku['token10totoken6']
                            token10totoken7 = ku['token10totoken7']

                            token10totoken8 = ku['token10totoken8']

                            token10totoken9 = ku['token10totoken9']
                            token10totoken3 = ku['token10totoken3']

                            if 'pricetoken1usd2' in globals() and 0 == 1:
                                try:
                                    if pricetoken1usd / pricetoken1usd2 >= 1.15 and pricetoken1usd > token1low and gelukt == 'buy ' + token1smallcasename:
                                        fasttoken1 = 1
                                        token1low = pricetoken1usd / 1.09
                                    if pricetoken2usd / pricetoken2usd2 >= 1.15 and pricetoken2usd > token2low and gelukt == 'buy ' + token2smallcasename:
                                        fasttoken2 = 1
                                        token2low = pricetoken2usd / 1.09
                                    if pricetoken3usd / pricetoken3usd2 >= 1.15 and pricetoken3usd > token3low and gelukt == 'buy ' + token3smallcasename:
                                        fasttoken3 = 1
                                        token3low = pricetoken3usd / 1.09
                                    if pricetoken4usd / pricetoken4usd2 >= 1.15 and pricetoken4usd > token4low and gelukt == 'buy ' + token4smallcasename:
                                        fasttoken4 = 1
                                        token4low = pricetoken4usd / 1.09
                                    if pricetoken5usd / pricetoken5usd2 >= 1.15 and pricetoken5usd > token5low and gelukt == 'buy ' + token5smallcasename:
                                        fasttoken5 = 1
                                        token5low = pricetoken5usd / 1.09
                                    if pricetoken6usd / pricetoken6usd2 >= 1.15 and pricetoken6usd > token6low and gelukt == 'buy ' + token6smallcasename:
                                        fasttoken6 = 1
                                        token6low = pricetoken6usd / 1.09
                                    if pricetoken7usd / pricetoken7usd2 >= 1.15 and pricetoken7usd > token7low and gelukt == 'buy ' + token7smallcasename:
                                        fasttoken7 = 1
                                        token7low = pricetoken7usd / 1.09
                                    if pricetoken8usd / pricetoken8usd2 >= 1.15 and pricetoken8usd > token8low and gelukt == 'buy ' + token8smallcasename:
                                        fasttoken8 = 1
                                        token8low = pricetoken8usd / 1.09
                                    if pricetoken9usd / pricetoken9usd2 >= 1.15 and pricetoken9usd > token9low and gelukt == 'buy ' + token9smallcasename:
                                        fasttoken9 = 1
                                        token9low = pricetoken9usd / 1.09
                                    if pricetoken10usd / pricetoken10usd2 >= 1.15 and pricetoken10usd > token10low and gelukt == 'buy ' + token10smallcasename:
                                        fasttoken10 = 1
                                        token10low = pricetoken10usd / 1.09
                                except:
                                    o = 0
                            if 1 == 1:
                                try:
                                    pricetoken1usd2 = pricetoken1usd
                                    pricetoken2usd2 = pricetoken2usd

                                    pricetoken3usd2 = pricetoken3usd

                                    pricetoken4usd2 = pricetoken4usd
                                    pricetoken5usd2 = pricetoken5usd
                                    pricetoken6usd2 = pricetoken6usd

                                    pricetoken7usd2 = pricetoken7usd
                                    pricetoken8usd2 = pricetoken8usd
                                    pricetoken9usd2 = pricetoken9usd

                                    pricetoken10usd2 = pricetoken10usd
                                except:
                                    o = 0


                        except Exception as e:
                            o = 0
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        if 'step' not in globals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            break

                        if "weergave1" not in locals():
                            print(str(strftime("%H:%M:%S", localtime())) + weergave + "  Current total balance($): $" +str(totaldollars))
                        if "weergave1" in locals():
                            if weergave != weergave1:
                                print(str(strftime("%H:%M:%S", localtime())) + weergave+ "  Current total balance($): $" +str(totaldollars))

                    except Exception as e:
                        exception_type, exception_object, exception_traceback = sys.exc_info()
                        if configfile.debugmode == '1':
                            print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        if e is not IndexError:
                            o = 0
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            if configfile.debugmode == '1':
                                print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                        if 'step' not in globals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            break
                        time.sleep(1)
                        notyet = 4
                    notyet == 3
                    if notyet == 3:
                        if 'step' not in globals():
                            step = 1
                        else:
                            step = step + 1
                        self.sig_step.emit(self.__id, 'step ' + str(step))
                        QCoreApplication.processEvents()

                        if self.__abort == True:
                            # note that "step" value will not necessarily be same for every thread
                            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                            break
                        oke = letstrade(keer, tradewithERCtoken1, tradewithERCtoken2, tradewithERCtoken3,
                                        tradewithERCtoken4,
                                        tradewithERCtoken5, tradewithERCtoken6, tradewithERCtoken9, tradewithERCtoken7,
                                        tradewithERCtoken8, tradewithERCtoken10, activatetoken1, activatetoken2,
                                        activatetoken3,
                                        activatetoken4, activatetoken5, activatetoken6, activatetoken9, activatetoken7,
                                        activatetoken8, activatetoken10, tradewithETHtoken1, tradewithETHtoken2,
                                        tradewithETHtoken3,
                                        tradewithETHtoken4, tradewithETHtoken5, tradewithETHtoken6, tradewithETHtoken9,
                                        tradewithETHtoken7, tradewithETHtoken8, tradewithETHtoken10, my_address, pk,
                                        max_slippage,
                                        infura_url, gelukt,
                                        tokentokennumerator,
                                        weergave, notyet, priceeth, pricetoken1usd, pricetoken2usd, token1totoken2,
                                        token2totoken1,
                                        pricetoken3usd, pricetoken4usd, pricetoken5usd,
                                        pricetoken6usd, pricetoken7usd, pricetoken8usd, pricetoken9usd, pricetoken10usd,
                                        token1totoken7, token1totoken8, token1totoken9,
                                        token1totoken3, token1totoken4, token1totoken5, token1totoken6, token1totoken10,
                                        token2totoken3, token2totoken4, token2totoken5,
                                        token2totoken6, token2totoken7, token2totoken8, token2totoken9, token2totoken10,
                                        token3totoken1, token3totoken2, token3totoken4,
                                        token3totoken5, token3totoken6, token3totoken7, token3totoken8, token3totoken9,
                                        token3totoken10, token4totoken1, token4totoken2,
                                        token4totoken3, token4totoken5, token4totoken6, token4totoken7, token4totoken8,
                                        token4totoken9, token4totoken10, token5totoken1,
                                        token5totoken2, token5totoken4, token5totoken3, token5totoken6, token5totoken7,
                                        token5totoken8, token5totoken9, token5totoken10,
                                        token6totoken1, token6totoken2, token6totoken4, token6totoken5, token6totoken3,
                                        token6totoken7, token6totoken8, token6totoken9,
                                        token6totoken10, token7totoken1, token7totoken2, token7totoken4, token7totoken5,
                                        token7totoken6, token7totoken3, token7totoken8,
                                        token7totoken9, token7totoken10, token8totoken1, token8totoken2, token8totoken4,
                                        token8totoken5, token8totoken6, token8totoken7,
                                        token8totoken3, token8totoken9, token8totoken10, token9totoken1, token9totoken2,
                                        token9totoken4, token9totoken5, token9totoken6,
                                        token9totoken7, token9totoken8, token9totoken3, token9totoken10,
                                        token10totoken1,
                                        token10totoken2, token10totoken4, token10totoken5,
                                        token10totoken6, token10totoken7, token10totoken8, token10totoken9,
                                        token10totoken3,
                                        token1address, token1smallcasename, token2address, token2smallcasename,
                                        token3address,
                                        token3smallcasename,
                                        token4address, token4smallcasename, token5address, token5smallcasename,
                                        token6address,
                                        token6smallcasename,
                                        token7address, token7smallcasename, token8address, token8smallcasename,
                                        token9address,
                                        token9smallcasename,
                                        token10address, token10smallcasename, token1high, token1low, token2high,
                                        token2low,
                                        token3high,
                                        token3low,
                                        token4high, token4low, token5high, token5low, token6high, token6low, token7high,
                                        token7low,
                                        token8high,
                                        token8low, token9high, token9low, token10high, token10low,
                                        incaseofbuyinghowmuch, timesleepaftertrade,
                                        ethtokeep, maincoinoption, fasttoken1, fasttoken2, fasttoken3, fasttoken4,
                                        fasttoken5, fasttoken6, fasttoken7, fasttoken8, fasttoken9, fasttoken10,
                                        stoplosstoken1, stoplosstoken2, stoplosstoken3, stoplosstoken4, stoplosstoken5,
                                        stoplosstoken6, stoplosstoken7, stoplosstoken8, stoplosstoken9, stoplosstoken10,
                                        stoplosschecktoken1, stoplosschecktoken2, stoplosschecktoken3,
                                        stoplosschecktoken4, stoplosschecktoken5, stoplosschecktoken6,
                                        stoplosschecktoken7, stoplosschecktoken8, stoplosschecktoken9,
                                        stoplosschecktoken10, token1decimals, token2decimals, token3decimals,
                                        token4decimals, token5decimals, token6decimals, token7decimals, token8decimals,
                                        token9decimals, token10decimals, speed,maxgwei,maxgweinumber,diffdeposit,diffdepositaddress)
                        gelukt = oke['gelukt']
                        gelukt2 = oke['gelukt']
                        keer = oke['keer']
                        fasttoken1 = oke['fasttoken1']
                        fasttoken2 = oke['fasttoken2']
                        fasttoken3 = oke['fasttoken3']
                        fasttoken4 = oke['fasttoken4']
                        fasttoken5 = oke['fasttoken5']
                        fasttoken6 = oke['fasttoken6']
                        fasttoken7 = oke['fasttoken7']
                        fasttoken8 = oke['fasttoken8']
                        fasttoken9 = oke['fasttoken9']
                        fasttoken10 = oke['fasttoken10']



            except Exception as e:
                if 'step' not in globals():
                    step = 1
                else:
                    step = step + 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()

                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
                    break
                exception_type, exception_object, exception_traceback = sys.exc_info()
                if configfile.debugmode == '1':
                    print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                if e is not IndexError:
                    o = 0
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    if configfile.debugmode == '1':
                        print(str(e) + ' on line: ' + str(exception_traceback.tb_lineno))
                    # o=0
                import socket


                def is_connected():
                    try:
                        # connect to the host -- tells us if the host is actually
                        # reachable
                        socket.create_connection(("1.1.1.1", 53))
                        return True
                    except OSError:
                        pass
                    return False


                internetcheck = is_connected()
                if internetcheck is False:
                    try:
                        time.sleep(5)
                    except:
                        time.sleep(5)
                if 'step' not in globals():
                    step = 1
                else:
                    step = step + 1
                self.sig_step.emit(self.__id, 'step ' + str(step))
                QCoreApplication.processEvents()
                if self.__abort == True:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
        if 'step' not in globals():
            step = 1
        else:
            step = step + 1
        self.sig_step.emit(self.__id, 'step ' + str(step))
        QCoreApplication.processEvents()

        if self.__abort == True:
            # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
        self.sig_done.emit(self.__id)

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True

# def funtie voor toevoeging tokens en automaties make trade met elkaar maken --> done alleen testen
# GUI maken en gebruiken mey pyqt desinger
# functie maken voor auto high low
# winst toevoegen tijdens runtime (hiervoor extra configfiletje maken)
# GUI maken mey pyqt desinger

def abort(self):
    self.__abort = True


class Ui_MainWindow(QGraphicsObject):
    NUM_THREADS = 1
    sig_abort_workers = pyqtSignal()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 702)
        form_layout = QVBoxLayout()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startbutton.setGeometry(QtCore.QRect(920, 590, 121, 71))
        self.startbutton.setObjectName("startbutton")
        self.stopbutton = QtWidgets.QPushButton(self.centralwidget)
        self.stopbutton.setGeometry(QtCore.QRect(750, 590, 171, 71))
        self.stopbutton.setObjectName("stopbutton")

        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(0, 0, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.oke = self.startbutton.clicked.connect(self.start_threads)
        self.stopbutton.clicked.connect(self.abort_workers)
        self.activatetoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken1.setGeometry(QtCore.QRect(440, 50, 91, 20))
        form_layout.addWidget(self.stopbutton)
        self.stopbutton.setDisabled(True)

        self.process = QtCore.QProcess(self)
        self.process.setProgram("dirb")
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.gweioption = QtWidgets.QComboBox(self.centralwidget)
        self.gweioption.setGeometry(QtCore.QRect(720, 380, 81, 21))
        self.gweioption.setMaxVisibleItems(4)
        self.gweioption.setObjectName("gweioption")
        self.maincoinoption = QtWidgets.QComboBox(self.centralwidget)
        self.maincoinoption.setGeometry(QtCore.QRect(130, 0, 81, 21))
        self.maincoinoption.setMaxVisibleItems(5)
        self.maincoinoption.setObjectName("maincoinoption")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(750, 370, 291, 16))
        self.label_17.setObjectName("label_17")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken1.setFont(font)
        self.log = QTextEdit()
        form_layout.addWidget(self.log)
        self.activatetoken1.setObjectName("activatetoken1")
        self.tradewithETHtoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken1.setGeometry(QtCore.QRect(540, 50, 141, 20))
        self.tradewithETHtoken1.setObjectName("tradewithETHtoken1")
        self.tradewithERCtoken1 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken1.setGeometry(QtCore.QRect(690, 50, 151, 20))
        self.tradewithERCtoken1.setObjectName("tradewithERCtoken1")
        self.tradewithETHtoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken2.setGeometry(QtCore.QRect(540, 80, 141, 20))
        self.tradewithETHtoken2.setObjectName("tradewithETHtoken2")
        self.activatetoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken2.setGeometry(QtCore.QRect(440, 80, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken2.setFont(font)
        self.activatetoken2.setObjectName("activatetoken2")
        self.tradewithERCtoken2 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken2.setGeometry(QtCore.QRect(690, 80, 141, 20))
        self.tradewithERCtoken2.setObjectName("tradewithERCtoken2")
        self.tradewithETHtoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken3.setGeometry(QtCore.QRect(540, 110, 141, 20))
        self.tradewithETHtoken3.setObjectName("tradewithETHtoken3")
        self.activatetoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken3.setGeometry(QtCore.QRect(440, 110, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken3.setFont(font)
        self.activatetoken3.setObjectName("activatetoken3")
        self.tradewithERCtoken3 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken3.setGeometry(QtCore.QRect(690, 110, 141, 20))
        self.tradewithERCtoken3.setObjectName("tradewithERCtoken3")
        self.tradewithERCtoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken5.setGeometry(QtCore.QRect(690, 170, 151, 20))
        self.tradewithERCtoken5.setObjectName("tradewithERCtoken5")
        self.tradewithETHtoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken4.setGeometry(QtCore.QRect(540, 140, 141, 20))
        self.tradewithETHtoken4.setObjectName("tradewithETHtoken4")
        self.tradewithERCtoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken6.setGeometry(QtCore.QRect(690, 200, 141, 20))
        self.tradewithERCtoken6.setObjectName("tradewithERCtoken6")
        self.tradewithETHtoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken6.setGeometry(QtCore.QRect(540, 200, 141, 20))
        self.tradewithETHtoken6.setObjectName("tradewithETHtoken6")
        self.activatetoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken4.setGeometry(QtCore.QRect(440, 140, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken4.setFont(font)
        self.activatetoken4.setObjectName("activatetoken4")
        self.activatetoken6 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken6.setGeometry(QtCore.QRect(440, 200, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken6.setFont(font)
        self.activatetoken6.setObjectName("activatetoken6")
        self.tradewithERCtoken4 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken4.setGeometry(QtCore.QRect(690, 140, 151, 20))
        self.tradewithERCtoken4.setObjectName("tradewithERCtoken4")
        self.tradewithETHtoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken5.setGeometry(QtCore.QRect(540, 170, 141, 20))
        self.tradewithETHtoken5.setObjectName("tradewithETHtoken5")
        self.activatetoken5 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken5.setGeometry(QtCore.QRect(440, 170, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken5.setFont(font)
        self.activatetoken5.setObjectName("activatetoken5")
        self.tradewithERCtoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken8.setGeometry(QtCore.QRect(690, 260, 141, 20))
        self.tradewithERCtoken8.setObjectName("tradewithERCtoken8")
        self.tradewithETHtoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken7.setGeometry(QtCore.QRect(540, 230, 141, 20))
        self.tradewithETHtoken7.setObjectName("tradewithETHtoken7")
        self.tradewithERCtoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken9.setGeometry(QtCore.QRect(690, 290, 141, 20))
        self.tradewithERCtoken9.setObjectName("tradewithERCtoken9")
        self.tradewithETHtoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken9.setGeometry(QtCore.QRect(540, 290, 141, 20))
        self.tradewithETHtoken9.setObjectName("tradewithETHtoken9")
        self.activatetoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken7.setGeometry(QtCore.QRect(440, 230, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken7.setFont(font)
        self.activatetoken7.setObjectName("activatetoken7")
        self.activatetoken9 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken9.setGeometry(QtCore.QRect(440, 290, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken9.setFont(font)
        self.activatetoken9.setObjectName("activatetoken9")
        self.tradewithERCtoken7 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken7.setGeometry(QtCore.QRect(690, 230, 141, 20))
        self.tradewithERCtoken7.setObjectName("tradewithERCtoken7")
        self.tradewithETHtoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken8.setGeometry(QtCore.QRect(540, 260, 141, 20))
        self.tradewithETHtoken8.setObjectName("tradewithETHtoken8")
        self.activatetoken8 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken8.setGeometry(QtCore.QRect(440, 260, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken8.setFont(font)
        self.activatetoken8.setObjectName("activatetoken8")
        self.activatetoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.activatetoken10.setGeometry(QtCore.QRect(440, 320, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.activatetoken10.setFont(font)
        self.activatetoken10.setObjectName("activatetoken10")
        self.tradewithETHtoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithETHtoken10.setGeometry(QtCore.QRect(540, 320, 141, 20))
        self.tradewithETHtoken10.setObjectName("tradewithETHtoken10")
        self.tradewithERCtoken10 = QtWidgets.QCheckBox(self.centralwidget)
        self.tradewithERCtoken10.setGeometry(QtCore.QRect(690, 320, 141, 20))
        self.tradewithERCtoken10.setObjectName("tradewithERCtoken10")

        try:
            self.stoplosstoken1 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken1.setGeometry(QtCore.QRect(840, 50, 111, 20))
            self.stoplosstoken2 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken2.setGeometry(QtCore.QRect(840, 80, 111, 20))
            self.stoplosstoken3 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken3.setGeometry(QtCore.QRect(840, 110, 111, 20))
            self.stoplosstoken4 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken4.setGeometry(QtCore.QRect(840, 140, 111, 20))
            self.stoplosstoken5 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken5.setGeometry(QtCore.QRect(840, 170, 111, 20))
            self.stoplosstoken6 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken6.setGeometry(QtCore.QRect(840, 200, 111, 20))
            self.stoplosstoken7 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken7.setGeometry(QtCore.QRect(840, 230, 111, 20))
            self.stoplosstoken8 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken8.setGeometry(QtCore.QRect(840, 260, 111, 20))
            self.stoplosstoken9 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken9.setGeometry(QtCore.QRect(840, 290, 111, 20))
            self.stoplosstoken10 = QtWidgets.QCheckBox(self.centralwidget)
            self.stoplosstoken10.setGeometry(QtCore.QRect(840, 320, 111, 20))

            self.debugmode = QtWidgets.QCheckBox(self.centralwidget)
            self.debugmode.setGeometry(QtCore.QRect(840, 10, 111, 20))
            self.token1stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token1stoploss.setGeometry(QtCore.QRect(960, 50, 71, 16))
            self.token1stoploss.setObjectName("token1stoploss")
            self.token2stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token2stoploss.setGeometry(QtCore.QRect(960, 80, 71, 16))
            self.token2stoploss.setObjectName("token2stoploss")
            self.token3stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token3stoploss.setGeometry(QtCore.QRect(960, 110, 71, 16))
            self.token3stoploss.setObjectName("token3stoploss")
            self.token4stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token4stoploss.setGeometry(QtCore.QRect(960, 140, 71, 16))
            self.token4stoploss.setObjectName("token4stoploss")
            self.token5stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token5stoploss.setGeometry(QtCore.QRect(960, 170, 71, 16))
            self.token5stoploss.setObjectName("token5stoploss")
            self.token6stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token6stoploss.setGeometry(QtCore.QRect(960, 200, 71, 16))
            self.token6stoploss.setObjectName("token6stoploss")
            self.token7stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token7stoploss.setGeometry(QtCore.QRect(960, 230, 71, 16))
            self.token7stoploss.setObjectName("token7stoploss")
            self.token8stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token8stoploss.setGeometry(QtCore.QRect(960, 260, 71, 16))
            self.token8stoploss.setObjectName("token8stoploss")
            self.token9stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token9stoploss.setGeometry(QtCore.QRect(960, 290, 71, 16))
            self.token9stoploss.setObjectName("token9stoploss")
            self.token10stoploss = QtWidgets.QLineEdit(self.centralwidget)
            self.token10stoploss.setGeometry(QtCore.QRect(960, 320, 71, 16))
            self.token10stoploss.setObjectName("token10stoploss")
            self.maxgwei = QtWidgets.QCheckBox(self.centralwidget)
            self.maxgwei.setGeometry(QtCore.QRect(710, 400, 111, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.maxgwei.setFont(font)
            self.maxgwei.setObjectName("maxgwei")
            self.maxgweinumber = QtWidgets.QLineEdit(self.centralwidget)
            self.maxgweinumber.setGeometry(QtCore.QRect(830, 400, 71, 16))
            self.maxgweinumber.setObjectName("maxgweinumber")
            self.diffdeposit = QtWidgets.QCheckBox(self.centralwidget)
            self.diffdeposit.setGeometry(QtCore.QRect(710, 420, 211, 20))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.diffdeposit.setFont(font)
            self.diffdeposit.setObjectName("diffdeposit")
            self.diffdepositaddress = QtWidgets.QLineEdit(self.centralwidget)
            self.diffdepositaddress.setGeometry(QtCore.QRect(930, 420, 111, 20))
            self.diffdepositaddress.setObjectName("diffdepositaddress")

        except Exception as e:
            print(e)

        if 1 == 1:
            self.token1stoploss.setText(configfile.token1stoploss)
        if 1 == 1:
            self.token2stoploss.setText(configfile.token2stoploss)
        if 1 == 1:
            self.token3stoploss.setText(configfile.token3stoploss)
        if 1 == 1:
            self.token4stoploss.setText(configfile.token4stoploss)
        if 1 == 1:
            self.token5stoploss.setText(configfile.token5stoploss)
        if 1 == 1:
            self.token6stoploss.setText(configfile.token6stoploss)
        if 1 == 1:
            self.token7stoploss.setText(configfile.token7stoploss)
        if 1 == 1:
            self.token8stoploss.setText(configfile.token8stoploss)
        if 1 == 1:
            self.token9stoploss.setText(configfile.token9stoploss)
        if 1 == 1:
            self.token10stoploss.setText(configfile.token10stoploss)

        self.token1low = QtWidgets.QLineEdit(self.centralwidget)
        self.token1low.setGeometry(QtCore.QRect(280, 50, 71, 16))
        self.token1low.setObjectName("token1low")
        if configfile.token1low != '0':
            self.token1low.setText(configfile.token1low)
        self.token1high = QtWidgets.QLineEdit(self.centralwidget)
        self.token1high.setGeometry(QtCore.QRect(360, 50, 71, 16))
        self.token1high.setObjectName("token1high")
        if configfile.token1high != '0':
            self.token1high.setText(configfile.token1high)
        self.token1ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token1ethaddress.setGeometry(QtCore.QRect(70, 50, 121, 16))
        self.token1ethaddress.setObjectName("token1ethaddress")
        if configfile.token1ethaddress != '0':
            self.token1ethaddress.setText(configfile.token1ethaddress)
        self.token2low = QtWidgets.QLineEdit(self.centralwidget)
        self.token2low.setGeometry(QtCore.QRect(280, 80, 71, 16))
        self.token2low.setObjectName("token2low")
        if configfile.token2low != '0':
            self.token2low.setText(configfile.token2low)
        self.token2ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token2ethaddress.setGeometry(QtCore.QRect(70, 80, 121, 16))
        self.token2ethaddress.setObjectName("token2ethaddress")
        if configfile.token2ethaddress != '0':
            self.token2ethaddress.setText(configfile.token2ethaddress)
        self.token2high = QtWidgets.QLineEdit(self.centralwidget)
        self.token2high.setGeometry(QtCore.QRect(360, 80, 71, 16))
        self.token2high.setObjectName("token2high")
        if configfile.token2high != '0':
            self.token2high.setText(configfile.token2high)
        self.token3low = QtWidgets.QLineEdit(self.centralwidget)
        self.token3low.setGeometry(QtCore.QRect(280, 110, 71, 16))
        self.token3low.setObjectName("token3low")
        if configfile.token3low != '0':
            self.token3low.setText(configfile.token3low)
        self.token3ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token3ethaddress.setGeometry(QtCore.QRect(70, 110, 121, 16))
        self.token3ethaddress.setObjectName("token3ethaddress")
        if configfile.token3ethaddress != '0':
            self.token3ethaddress.setText(configfile.token3ethaddress)
        self.token3high = QtWidgets.QLineEdit(self.centralwidget)
        self.token3high.setGeometry(QtCore.QRect(360, 110, 71, 16))
        self.token3high.setObjectName("token3high")
        if configfile.token3high != '0':
            self.token3high.setText(configfile.token3high)
        self.token6high = QtWidgets.QLineEdit(self.centralwidget)
        self.token6high.setGeometry(QtCore.QRect(360, 200, 71, 16))
        self.token6high.setObjectName("token6high")
        if configfile.token6high != '0':
            self.token6high.setText(configfile.token6high)
        self.token5high = QtWidgets.QLineEdit(self.centralwidget)
        self.token5high.setGeometry(QtCore.QRect(360, 170, 71, 16))
        self.token5high.setObjectName("token5high")
        if configfile.token5high != '0':
            self.token5high.setText(configfile.token5high)
        self.token4low = QtWidgets.QLineEdit(self.centralwidget)
        self.token4low.setGeometry(QtCore.QRect(280, 140, 71, 16))
        self.token4low.setObjectName("token4low")
        if configfile.token4low != '0':
            self.token4low.setText(configfile.token4low)
        self.token5low = QtWidgets.QLineEdit(self.centralwidget)
        self.token5low.setGeometry(QtCore.QRect(280, 170, 71, 16))
        self.token5low.setObjectName("token5low")
        if configfile.token5low != '0':
            self.token5low.setText(configfile.token5low)
        self.token4high = QtWidgets.QLineEdit(self.centralwidget)
        self.token4high.setGeometry(QtCore.QRect(360, 140, 71, 16))
        self.token4high.setObjectName("token4high")
        if configfile.token4high != '0':
            self.token4high.setText(configfile.token4high)
        self.token4ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token4ethaddress.setGeometry(QtCore.QRect(70, 140, 121, 16))
        self.token4ethaddress.setObjectName("token4ethaddress")
        if configfile.token4ethaddress != '0':
            self.token4ethaddress.setText(configfile.token4ethaddress)
        self.token6low = QtWidgets.QLineEdit(self.centralwidget)
        self.token6low.setGeometry(QtCore.QRect(280, 200, 71, 16))
        self.token6low.setObjectName("token6low")
        if configfile.token6low != '0':
            self.token6low.setText(configfile.token6low)
        self.token5ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token5ethaddress.setGeometry(QtCore.QRect(70, 170, 121, 16))
        self.token5ethaddress.setObjectName("token5ethaddress")
        if configfile.token5ethaddress != '0':
            self.token5ethaddress.setText(configfile.token5ethaddress)
        self.token6ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token6ethaddress.setGeometry(QtCore.QRect(70, 200, 121, 16))
        self.token6ethaddress.setObjectName("token6ethaddress")
        if configfile.token6ethaddress != '0':
            self.token6ethaddress.setText(configfile.token6ethaddress)
        self.token9high = QtWidgets.QLineEdit(self.centralwidget)
        self.token9high.setGeometry(QtCore.QRect(360, 290, 71, 16))
        self.token9high.setObjectName("token9high")
        if configfile.token9high != '0':
            self.token9high.setText(configfile.token9high)
        self.token8high = QtWidgets.QLineEdit(self.centralwidget)
        self.token8high.setGeometry(QtCore.QRect(360, 260, 71, 16))
        self.token8high.setObjectName("token8high")
        if configfile.token8high != '0':
            self.token8high.setText(configfile.token8high)
        self.token7low = QtWidgets.QLineEdit(self.centralwidget)
        self.token7low.setGeometry(QtCore.QRect(280, 230, 71, 16))
        self.token7low.setObjectName("token7low")
        if configfile.token7low != '0':
            self.token7low.setText(configfile.token7low)
        self.token8low = QtWidgets.QLineEdit(self.centralwidget)
        self.token8low.setGeometry(QtCore.QRect(280, 260, 71, 16))
        self.token8low.setObjectName("token8low")
        if configfile.token8low != '0':
            self.token8low.setText(configfile.token8low)
        self.token7high = QtWidgets.QLineEdit(self.centralwidget)
        self.token7high.setGeometry(QtCore.QRect(360, 230, 71, 16))
        self.token7high.setObjectName("token7high")
        if configfile.token7high != '0':
            self.token7high.setText(configfile.token7high)
        self.token7ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token7ethaddress.setGeometry(QtCore.QRect(70, 230, 121, 16))
        self.token7ethaddress.setObjectName("token7ethaddress")
        if configfile.token7ethaddress != '0':
            self.token7ethaddress.setText(configfile.token7ethaddress)
        self.token9low = QtWidgets.QLineEdit(self.centralwidget)
        self.token9low.setGeometry(QtCore.QRect(280, 290, 71, 16))
        self.token9low.setObjectName("token9low")
        if configfile.token9low != '0':
            self.token9low.setText(configfile.token9low)
        self.token8ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token8ethaddress.setGeometry(QtCore.QRect(70, 260, 121, 16))
        self.token8ethaddress.setObjectName("token8ethaddress")
        if configfile.token8ethaddress != '0':
            self.token8ethaddress.setText(configfile.token8ethaddress)
        self.token9ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token9ethaddress.setGeometry(QtCore.QRect(70, 290, 121, 16))
        self.token9ethaddress.setObjectName("token9ethaddress")
        if configfile.token9ethaddress != '0':
            self.token9ethaddress.setText(configfile.token9ethaddress)
        self.token10high = QtWidgets.QLineEdit(self.centralwidget)
        self.token10high.setGeometry(QtCore.QRect(360, 320, 71, 16))
        self.token10high.setObjectName("token10high")
        if configfile.token10high != '0':
            self.token10high.setText(configfile.token10high)
        self.token10ethaddress = QtWidgets.QLineEdit(self.centralwidget)
        self.token10ethaddress.setGeometry(QtCore.QRect(70, 320, 121, 16))
        self.token10ethaddress.setObjectName("token10ethaddress")
        if configfile.token10ethaddress != '0':
            self.token10ethaddress.setText(configfile.token10ethaddress)
        self.token10low = QtWidgets.QLineEdit(self.centralwidget)
        self.token10low.setGeometry(QtCore.QRect(280, 320, 71, 16))
        self.token10low.setObjectName("token10low")
        if configfile.token10low != '0':
            self.token10low.setText(configfile.token10low)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 50, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 80, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 140, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 110, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 200, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(0, 170, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(0, 260, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(0, 230, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(0, 320, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(0, 290, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(70, 30, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setGeometry(QtCore.QRect(370, 30, 61, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(290, 30, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_8.setFont(font)
        self.label_7.setFont(font)
        self.label_12.setFont(font)
        self.label_10.setFont(font)
        self.label_11.setFont(font)
        self.label_12.setFont(font)
        self.label_13.setFont(font)

        self.label_13.setObjectName("label_13")
        self.currentstatus = QtWidgets.QTextBrowser(self.centralwidget)
        self.currentstatus.setGeometry(QtCore.QRect(0, 450, 1051, 141))
        self.currentstatus.setObjectName("currentstatus")

        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(600, 370, 81, 16))
        self.label_14.setObjectName("label_14")
        self.secondscheckingprice = QtWidgets.QSpinBox(self.centralwidget)
        self.secondscheckingprice.setGeometry(QtCore.QRect(0, 370, 31, 16))
        self.secondscheckingprice.setObjectName("secondscheckingprice")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 350, 1041, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.sleepbox = QtWidgets.QLabel(self.centralwidget)
        self.sleepbox.setGeometry(QtCore.QRect(50, 370, 341, 16))
        self.sleepbox.setObjectName("sleepbox")
        self.tokentokennumerator = QtWidgets.QLineEdit(self.centralwidget)
        self.tokentokennumerator.setGeometry(QtCore.QRect(0, 390, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)

        self.tokentokennumerator.setObjectName("tokentokennumerator")
        self.tokentokennumerator.setFont(font)

        self.tokentokennumeratorbox = QtWidgets.QLabel(self.centralwidget)
        self.tokentokennumeratorbox.setGeometry(QtCore.QRect(50, 390, 321, 16))
        self.tokentokennumeratorbox.setObjectName("tokentokennumeratorbox")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tokentokennumeratorbox.setFont(font)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(-40, 440, 1081, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(710, 360, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.infurabox = QtWidgets.QLabel(self.centralwidget)
        self.infurabox.setGeometry(QtCore.QRect(230, 410, 81, 16))
        self.infurabox.setObjectName("infurabox")
        self.infurabox.setFont(font)
        self.infuraurl = QtWidgets.QLineEdit(self.centralwidget)
        self.infuraurl.setGeometry(QtCore.QRect(0, 410, 221, 16))
        self.infuraurl.setObjectName("infuraurl")

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(200, 30, 81, 16))
        self.label_15.setObjectName("label_15")
        self.label_15.setFont(font)
        self.token1name = QtWidgets.QLineEdit(self.centralwidget)
        self.token1name.setGeometry(QtCore.QRect(200, 50, 71, 16))
        self.token1name.setObjectName("token1name")
        self.token2name = QtWidgets.QLineEdit(self.centralwidget)
        self.token2name.setGeometry(QtCore.QRect(200, 80, 71, 16))
        self.token2name.setObjectName("token2name")
        self.token3name = QtWidgets.QLineEdit(self.centralwidget)
        self.token3name.setGeometry(QtCore.QRect(200, 110, 71, 16))
        self.token3name.setObjectName("token3name")
        self.token4name = QtWidgets.QLineEdit(self.centralwidget)
        self.token4name.setGeometry(QtCore.QRect(200, 140, 71, 16))
        self.token4name.setObjectName("token4name")
        self.token5name = QtWidgets.QLineEdit(self.centralwidget)
        self.token5name.setGeometry(QtCore.QRect(200, 170, 71, 16))
        self.token5name.setObjectName("token5name")
        self.token6name = QtWidgets.QLineEdit(self.centralwidget)
        self.token6name.setGeometry(QtCore.QRect(200, 200, 71, 16))
        self.token6name.setObjectName("token6name")
        self.token7name = QtWidgets.QLineEdit(self.centralwidget)
        self.token7name.setGeometry(QtCore.QRect(200, 230, 71, 16))
        self.token7name.setObjectName("token7name")
        self.token8name = QtWidgets.QLineEdit(self.centralwidget)
        self.token8name.setGeometry(QtCore.QRect(200, 260, 71, 16))
        self.token8name.setObjectName("token8name")
        self.token9name = QtWidgets.QLineEdit(self.centralwidget)
        self.token9name.setGeometry(QtCore.QRect(200, 290, 71, 16))
        self.token9name.setObjectName("token9name")
        self.token10name = QtWidgets.QLineEdit(self.centralwidget)
        self.token10name.setGeometry(QtCore.QRect(200, 320, 71, 16))
        self.token10name.setObjectName("token10name")
        self.updatename = QtWidgets.QPushButton(self.centralwidget)
        self.updatename.setGeometry(QtCore.QRect(200, 340, 81, 20))
        self.updatename.setObjectName("updatename")
        self.secondscheckingprice_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.secondscheckingprice_2.setGeometry(QtCore.QRect(400, 370, 31, 16))
        self.secondscheckingprice_2.setObjectName("secondscheckingprice_2")
        self.sleepbox_2 = QtWidgets.QLabel(self.centralwidget)
        self.sleepbox_2.setGeometry(QtCore.QRect(450, 370, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sleepbox_2.setFont(font)
        self.sleepbox_2.setObjectName("sleepbox_2")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(380, 360, 20, 81))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.Maxslippage = QtWidgets.QLineEdit(self.centralwidget)
        self.Maxslippage.setGeometry(QtCore.QRect(400, 390, 31, 16))
        self.Maxslippage.setObjectName("Maxslippage")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(450, 390, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 410, 31, 16))
        self.lineEdit.setObjectName("lineEdit")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(450, 410, 271, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.oke2 = self.updatename.clicked.connect(self.updatenames)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1056, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.log = QTextEdit()
        form_layout.addWidget(self.log)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(690, 360, 20, 91))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.progress = QTextEdit()
        form_layout.addWidget(self.progress)
        self.retranslateUi(MainWindow)
        QThread.currentThread().setObjectName('main')  # threads can be named, useful for log output
        self.__workers_done = None
        self.__threads = None
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        if configfile.secondscheckingprice_2 != '0':
            self.secondscheckingprice_2.setValue(int(configfile.secondscheckingprice_2))
        if configfile.secondscheckingprice != '0':
            self.secondscheckingprice.setValue(int(configfile.secondscheckingprice))
        if configfile.infuraurl != '0':
            self.infuraurl.setText(str(configfile.infuraurl))
        if configfile.tokentokennumerator != '0':
            self.tokentokennumerator.setText(str(configfile.tokentokennumerator))

        if configfile.maxgweinumber != '0':
            self.maxgweinumber.setText(str(configfile.maxgweinumber))
        if configfile.diffdepositaddress!= '0':
            self.diffdepositaddress.setText(str(configfile.maxgweinumber))

        try:
            if configfile.maxgwei != '0':
                self.maxgwei.setChecked(1)
        except:
            o = 0
        try:
            if configfile.diffdeposit != '0':
                self.diffdeposit.setChecked(1)
        except:
            o = 0
        try:
            if configfile.activatetoken1 != '0':
                self.activatetoken1.setChecked(1)
        except:
            o = 0
        try:
            if configfile.debugmode != '0':
                self.debugmode.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithETHtoken1 != '0':
                self.tradewithETHtoken1.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken1 != '0':
                self.tradewithERCtoken1.setChecked(1)
        except:
            o = 0
        try:
            if configfile.activatetoken2 != '0':
                self.activatetoken2.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken2 != '0':
                self.tradewithETHtoken2.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken2 != '0':
                self.tradewithERCtoken2.setChecked(1)
        except:
            o = 0
        try:
            if configfile.activatetoken3 != '0':
                self.activatetoken3.setChecked(1)
        except:
            o = 0

        try:
            if configfile.stoplosstoken1 != '0':
                self.stoplosstoken1.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken2 != '0':
                self.stoplosstoken2.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken3 != '0':
                self.stoplosstoken3.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken4 != '0':
                self.stoplosstoken4.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken5 != '0':
                self.stoplosstoken5.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken6 != '0':
                self.stoplosstoken6.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken7 != '0':
                self.stoplosstoken7.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken8 != '0':
                self.stoplosstoken8.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken9 != '0':
                self.stoplosstoken9.setChecked(1)
        except:
            o = 0
        try:
            if configfile.stoplosstoken10 != '0':
                self.stoplosstoken10.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken3 != '0':
                self.tradewithETHtoken3.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken3 != '0':
                self.tradewithERCtoken3.setChecked(1)
        except:
            o = 0
        try:
            if configfile.activatetoken4 != '0':
                self.activatetoken4.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken4 != '0':
                self.tradewithETHtoken4.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken4 != '0':
                self.tradewithERCtoken4.setChecked(1)
        except:
            o = 0
        try:
            if configfile.activatetoken5 != '0':
                self.activatetoken5.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken5 != '0':
                self.tradewithETHtoken5.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken5 != '0':
                self.tradewithERCtoken5.setChecked(1)
        except:
            o = 0

        try:
            if configfile.activatetoken6 != '0':
                self.activatetoken6.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken6 != '0':
                self.tradewithETHtoken6.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken6 != '0':
                self.tradewithERCtoken6.setChecked(1)
        except:
            o = 0

        try:
            if configfile.activatetoken7 != '0':
                self.activatetoken7.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken7 != '0':
                self.tradewithETHtoken7.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken7 != '0':
                self.tradewithERCtoken7.setChecked(1)
        except:
            o = 0

        try:
            if configfile.activatetoken8 != '0':
                self.activatetoken8.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken8 != '0':
                self.tradewithETHtoken8.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken8 != '0':
                self.tradewithERCtoken8.setChecked(1)
        except:
            o = 0

        try:
            if configfile.activatetoken9 != '0':
                self.activatetoken9.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken9 != '0':
                self.tradewithETHtoken9.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken9 != '0':
                self.tradewithERCtoken9.setChecked(1)
        except:
            o = 0

        try:
            if configfile.activatetoken10 != '0':
                self.activatetoken10.setChecked(1)
        except:
            o = 0

        try:
            if configfile.tradewithETHtoken10 != '0':
                self.tradewithETHtoken10.setChecked(1)
        except:
            o = 0
        try:
            if configfile.tradewithERCtoken10 != '0':
                self.tradewithERCtoken10.setChecked(1)
        except:
            o = 0
        if configfile.token1name != '0' and self.token1ethaddress.text() != '':
            self.token1name.setText(configfile.token1name)
        if configfile.max_slippage != '0':
            self.Maxslippage.setText(configfile.max_slippage)
        if configfile.ethtokeep != '0':
            self.lineEdit.setText(configfile.ethtokeep)
        if configfile.token2name != '0' and self.token2ethaddress.text() != '':
            self.token2name.setText(configfile.token2name)
        if configfile.token3name != '0' and self.token3ethaddress.text() != '':
            self.token3name.setText(configfile.token3name)
        if configfile.token4name != '0' and self.token4ethaddress.text() != '':
            self.token4name.setText(configfile.token4name)
        if configfile.token5name != '0' and self.token5ethaddress.text() != '':
            self.token5name.setText(configfile.token5name)
        if configfile.token6name != '0' and self.token6ethaddress.text() != '':
            self.token6name.setText(configfile.token6name)
        if configfile.token7name != '0' and self.token7ethaddress.text() != '':
            self.token7name.setText(configfile.token7name)
        if configfile.token8name != '0' and self.token8ethaddress.text() != '':
            self.token8name.setText(configfile.token8name)
        if configfile.token9name != '0' and self.token9ethaddress.text() != '':
            self.token9name.setText(configfile.token9name)
        if configfile.token10name != '0' and self.token10ethaddress.text() != '':
            self.token10name.setText(configfile.token10name)
        self.token1name.setReadOnly(True)
        self.token2name.setReadOnly(True)
        self.token3name.setReadOnly(True)
        self.token4name.setReadOnly(True)
        self.token5name.setReadOnly(True)
        self.token6name.setReadOnly(True)
        self.token7name.setReadOnly(True)
        self.token8name.setReadOnly(True)
        self.token9name.setReadOnly(True)
        self.token10name.setReadOnly(True)
        self.sleepbox.setFont(font)
        self.label_18.setFont(font)

        self.gweioption.addItem('Fastest/Trader', userData='Fastest')
        self.gweioption.addItem('Fast', userData='Fast')
        self.gweioption.addItem('Standard', userData='Standard')
        self.gweioption.addItem('Cheap', userData='Cheap')
        self.maincoinoption.addItem('Ethereum', userData='Ethereum')
        self.maincoinoption.addItem('USDT', userData='USDT')
        self.maincoinoption.addItem('DAI', userData='DAI')
        self.maincoinoption.addItem('USDC', userData='USDC')
        self.maincoinoption.addItem('wBTC', userData='wBTC')
        if configfile.speed == 'fastest':
            self.gweioption.setCurrentIndex(0)
        if configfile.speed == 'fast':
            self.gweioption.setCurrentIndex(1)
        if configfile.speed == 'average':
            self.gweioption.setCurrentIndex(2)
        if configfile.speed == 'safeLow':
            self.gweioption.setCurrentIndex(3)
        if configfile.maincoinoption == 'Ethereum':
            self.maincoinoption.setCurrentIndex(0)
        if configfile.maincoinoption == 'USDT':
            self.maincoinoption.setCurrentIndex(1)
        if configfile.maincoinoption == 'DAI':
            self.maincoinoption.setCurrentIndex(2)
        if configfile.maincoinoption == 'USDC':
            self.maincoinoption.setCurrentIndex(3)
        if configfile.maincoinoption == 'wBTC':
            self.maincoinoption.setCurrentIndex(4)
        self.tradewithETHtoken1.setFont(font)
        self.tradewithETHtoken2.setFont(font)
        self.tradewithETHtoken3.setFont(font)
        self.tradewithETHtoken4.setFont(font)
        self.tradewithETHtoken5.setFont(font)
        self.tradewithETHtoken6.setFont(font)
        self.tradewithETHtoken7.setFont(font)
        self.tradewithETHtoken8.setFont(font)
        self.tradewithETHtoken9.setFont(font)
        self.tradewithETHtoken10.setFont(font)
        self.tradewithERCtoken1.setFont(font)
        self.tradewithERCtoken2.setFont(font)
        self.tradewithERCtoken3.setFont(font)
        self.tradewithERCtoken4.setFont(font)
        self.tradewithERCtoken5.setFont(font)
        self.tradewithERCtoken6.setFont(font)
        self.tradewithERCtoken7.setFont(font)
        self.tradewithERCtoken8.setFont(font)
        self.tradewithERCtoken9.setFont(font)
        self.tradewithERCtoken10.setFont(font)
        self.stoplosstoken10.setFont(font)
        self.stoplosstoken9.setFont(font)
        self.stoplosstoken8.setFont(font)
        self.stoplosstoken7.setFont(font)
        self.stoplosstoken6.setFont(font)
        self.stoplosstoken5.setFont(font)
        self.stoplosstoken4.setFont(font)
        self.stoplosstoken3.setFont(font)
        self.stoplosstoken2.setFont(font)
        self.stoplosstoken1.setFont(font)
        self.gweioption.setFont(font)
        self.maincoinoption.setFont(font)
        self.token1low.setFont(font)
        self.token2low.setFont(font)
        self.token3low.setFont(font)
        self.token4low.setFont(font)
        self.token5low.setFont(font)
        self.token6low.setFont(font)
        self.token7low.setFont(font)
        self.token8low.setFont(font)
        self.token9low.setFont(font)
        self.token10low.setFont(font)
        self.token1high.setFont(font)
        self.token2high.setFont(font)
        self.token3high.setFont(font)
        self.token4high.setFont(font)
        self.token5high.setFont(font)
        self.token6high.setFont(font)
        self.token7high.setFont(font)
        self.token8high.setFont(font)
        self.token9high.setFont(font)
        self.token10high.setFont(font)
        self.token1ethaddress.setFont(font)
        self.token2ethaddress.setFont(font)
        self.token3ethaddress.setFont(font)
        self.token4ethaddress.setFont(font)
        self.token5ethaddress.setFont(font)
        self.token6ethaddress.setFont(font)
        self.token7ethaddress.setFont(font)
        self.token8ethaddress.setFont(font)
        self.currentstatus.setFont(font)
        self.token9ethaddress.setFont(font)
        self.token10ethaddress.setFont(font)
        self.secondscheckingprice.setFont(font)
        self.secondscheckingprice_2.setFont(font)
        self.tokentokennumerator.setFont(font)
        self.Maxslippage.setFont(font)
        self.lineEdit.setFont(font)
        self.infuraurl.setFont(font)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.updatename.setFont(font)
        self.retranslateUi(MainWindow)
        sys.stdout = Port(self.currentstatus)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Uniswap trader GUI"))
        self.startbutton.setText(_translate("MainWindow", "Start"))
        self.activatetoken1.setText(_translate("MainWindow", "Activate"))
        self.tradewithETHtoken1.setText(_translate("MainWindow", "Trade with ETH"))
        self.tradewithERCtoken1.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken2.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken2.setText(_translate("MainWindow", "Activate"))
        self.tradewithERCtoken2.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken3.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken3.setText(_translate("MainWindow", "Activate"))
        self.tradewithERCtoken3.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithERCtoken5.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken4.setText(_translate("MainWindow", "Trade with ETH"))
        self.tradewithERCtoken6.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken6.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken4.setText(_translate("MainWindow", "Activate"))
        self.activatetoken6.setText(_translate("MainWindow", "Activate"))
        self.tradewithERCtoken4.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken5.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken5.setText(_translate("MainWindow", "Activate"))
        self.tradewithERCtoken8.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken7.setText(_translate("MainWindow", "Trade with ETH"))
        self.tradewithERCtoken9.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken9.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken7.setText(_translate("MainWindow", "Activate"))
        self.activatetoken9.setText(_translate("MainWindow", "Activate"))
        self.tradewithERCtoken7.setText(_translate("MainWindow", "Trade with ERC"))
        self.tradewithETHtoken8.setText(_translate("MainWindow", "Trade with ETH"))
        self.activatetoken8.setText(_translate("MainWindow", "Activate"))
        self.activatetoken10.setText(_translate("MainWindow", "Activate"))
        self.tradewithETHtoken10.setText(_translate("MainWindow", "Trade with ETH"))
        self.tradewithERCtoken10.setText(_translate("MainWindow", "Trade with ERC"))
        self.label.setText(_translate("MainWindow", "Token 1"))
        self.label_2.setText(_translate("MainWindow", "Token 2"))
        self.label_3.setText(_translate("MainWindow", "Token 4"))
        self.label_4.setText(_translate("MainWindow", "Token 3"))
        self.label_5.setText(_translate("MainWindow", "Token 6"))
        self.label_6.setText(_translate("MainWindow", "Token 5"))
        self.label_7.setText(_translate("MainWindow", "Token 8"))
        self.label_8.setText(_translate("MainWindow", "Token 7"))
        self.label_9.setText(_translate("MainWindow", "Token 10"))
        self.label_10.setText(_translate("MainWindow", "Token 9"))
        self.label_11.setText(_translate("MainWindow", "Token address"))
        self.label_12.setText(_translate("MainWindow", "High($)"))
        self.label_13.setText(_translate("MainWindow", "Low($)"))
        self.stopbutton.setText(_translate("MainWindow", "Stop"))
        self.sleepbox.setText(_translate("MainWindow", "Seconds between checking price (min. 1 sec)"))
        self.tokentokennumeratorbox.setText(_translate("MainWindow", "Tokentokennumerator (3.3= standard)"))
        self.infurabox.setText(_translate("MainWindow", "Infura URL"))
        self.label_15.setText(_translate("MainWindow", "Name"))
        self.sleepbox_2.setText(_translate("MainWindow", "Seconds waiting after trade"))
        self.label_14.setText(_translate("MainWindow", "Max slippage (1%=0.01)"))
        self.label_16.setText(_translate("MainWindow", "$ to keep in ETH after trade"))
        self.label_17.setText(_translate("MainWindow", "GWEI option (see ethgasstattion.com)"))
        self.label_18.setText(_translate("MainWindow", "Main coin/token"))
        self.stoplosstoken1.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken2.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken3.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken6.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken4.setText(_translate("MainWindow", "Stoploss($):"))
        self.maxgwei.setText(_translate("MainWindow", "Max GWEI:"))
        self.diffdeposit.setText(_translate("MainWindow", "Different deposit address:"))
        self.debugmode.setText(_translate("MainWindow", "Debug mode"))
        self.stoplosstoken5.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken9.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken7.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken8.setText(_translate("MainWindow", "Stoploss($):"))
        self.stoplosstoken10.setText(_translate("MainWindow", "Stoploss($):"))
        self.updatename.setText(_translate("MainWindow", "Update names"))

    def updatenames(self):
        try:
            token1smallcasename = 0
            token1smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token1ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token1name.setText(token1smallcasename)
        except:
            pass
        try:
            token2smallcasename = 0
            token2smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token2ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token2name.setText(token2smallcasename)
        except:
            pass
        try:
            token3smallcasename = 0
            token3smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token3ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token3name.setText(token3smallcasename)
        except:
            pass
        try:
            token4smallcasename = 0
            token4smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token4ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token4name.setText(token4smallcasename)
        except:
            pass
        try:
            token5smallcasename = 0
            token5smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token5ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token5name.setText(token5smallcasename)
        except:
            pass
        try:
            token6smallcasename = 0
            token6smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token6ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token6name.setText(token6smallcasename)
        except:
            pass
        try:
            token7smallcasename = 0
            token7smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token7ethaddress.text(),
                                                             id='ethereum')['symbol']
            self.token7name.setText(token7smallcasename)
        except:
            pass
        try:
            token8smallcasename = 0
            token8smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token8ethaddress.text(),
                                                             id='ethereum')[
                    'symbol']
            self.token8name.setText(token8smallcasename)
        except:
            pass
        try:
            token9smallcasename = 0
            token9smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token9ethaddress.text(),
                                                             id='ethereum')[
                    'symbol']
            self.token9name.setText(token9smallcasename)
        except:
            pass
        try:
            token10smallcasename = 0
            token10smallcasename = \
                cg.get_coin_info_from_contract_address_by_id(contract_address=self.token10ethaddress.text(),
                                                             id='ethereum')[
                    'symbol']
            self.token10name.setText(token10smallcasename)
        except:
            pass
        if token1smallcasename == 0:
            self.token1name.setText('')
        if token2smallcasename == 0:
            self.token2name.setText('')
        if token3smallcasename == 0:
            self.token3name.setText('')
        if token4smallcasename == 0:
            self.token4name.setText('')
        if token5smallcasename == 0:
            self.token5name.setText('')
        if token6smallcasename == 0:
            self.token6name.setText('')
        if token7smallcasename == 0:
            self.token7name.setText('')
        if token8smallcasename == 0:
            self.token8name.setText('')
        if token9smallcasename == 0:
            self.token9name.setText('')
        if token10smallcasename == 0:
            self.token10name.setText('')

    @QtCore.pyqtSlot()
    def start_threads(self):
        try:
            print('Starting bot')
            maincoinoption = self.maincoinoption.currentText()
            if self.gweioption.currentText() == 'Fastest/Trader':
                speed = 'fastest'
            if self.gweioption.currentText() == 'Fast':
                speed = 'fast'
            if self.gweioption.currentText() == 'Standard':
                speed = 'average'
            if self.gweioption.currentText() == 'Cheap':
                speed = 'safeLow'
        except Exception as e:
            o = 0
        try:
            self.secondscheckingprice_2.setEnabled(False)
            self.secondscheckingprice.setEnabled(False)
            self.infuraurl.setEnabled(False)
            self.tokentokennumerator.setEnabled(False)
            self.activatetoken1.setEnabled(False)
            self.tradewithETHtoken1.setEnabled(False)
            self.tradewithERCtoken1.setEnabled(False)
            self.token1ethaddress.setReadOnly(True)
            self.token1low.setReadOnly(True)
            self.token1high.setReadOnly(True)
            self.token1ethaddress.setDisabled(True)
            self.token1low.setDisabled(True)
            self.token1high.setDisabled(True)
            self.debugmode.setDisabled(True)
            self.maxgwei.setDisabled(True)
            self.diffdeposit.setDisabled(True)
            self.maxgweinumber.setReadOnly(True)
            self.diffdepositaddress.setReadOnly(True)
            self.maxgweinumber.setDisabled(True)
            self.diffdepositaddress.setDisabled(True)

            self.activatetoken2.setEnabled(False)
            self.tradewithETHtoken2.setEnabled(False)
            self.tradewithERCtoken2.setEnabled(False)
            self.token2ethaddress.setReadOnly(True)
            self.token2low.setReadOnly(True)
            self.token2high.setReadOnly(True)
            self.token2ethaddress.setDisabled(True)
            self.token2low.setDisabled(True)
            self.token2high.setDisabled(True)

            self.activatetoken3.setEnabled(False)
            self.tradewithETHtoken3.setEnabled(False)
            self.tradewithERCtoken3.setEnabled(False)
            self.token3ethaddress.setReadOnly(True)
            self.token3low.setReadOnly(True)
            self.token3high.setReadOnly(True)
            self.token3ethaddress.setDisabled(True)
            self.token3low.setDisabled(True)
            self.token3high.setDisabled(True)

            self.activatetoken4.setEnabled(False)
            self.tradewithETHtoken4.setEnabled(False)
            self.tradewithERCtoken4.setEnabled(False)
            self.token4ethaddress.setReadOnly(True)
            self.token4low.setReadOnly(True)
            self.token4high.setReadOnly(True)
            self.token4ethaddress.setDisabled(True)
            self.token4low.setDisabled(True)
            self.token4high.setDisabled(True)

            self.activatetoken5.setEnabled(False)
            self.tradewithETHtoken5.setEnabled(False)
            self.tradewithERCtoken5.setEnabled(False)
            self.token5ethaddress.setReadOnly(True)
            self.token5low.setReadOnly(True)
            self.token5high.setReadOnly(True)
            self.token5ethaddress.setDisabled(True)
            self.token5low.setDisabled(True)
            self.token5high.setDisabled(True)

            self.activatetoken6.setEnabled(False)
            self.tradewithETHtoken6.setEnabled(False)
            self.tradewithERCtoken6.setEnabled(False)
            self.token6ethaddress.setReadOnly(True)
            self.token6low.setReadOnly(True)
            self.token6high.setReadOnly(True)
            self.token6ethaddress.setDisabled(True)
            self.token6low.setDisabled(True)
            self.token6high.setDisabled(True)

            self.activatetoken7.setEnabled(False)
            self.tradewithETHtoken7.setEnabled(False)
            self.tradewithERCtoken7.setEnabled(False)
            self.token7ethaddress.setReadOnly(True)
            self.token7low.setReadOnly(True)
            self.token7high.setReadOnly(True)
            self.token7ethaddress.setDisabled(True)
            self.token7low.setDisabled(True)
            self.token7high.setDisabled(True)

            self.updatename.setDisabled(True)

            self.activatetoken8.setEnabled(False)
            self.tradewithETHtoken8.setEnabled(False)
            self.tradewithERCtoken8.setEnabled(False)
            self.token8ethaddress.setReadOnly(True)
            self.token8low.setReadOnly(True)
            self.token8high.setReadOnly(True)
            self.token8ethaddress.setDisabled(True)
            self.token8low.setDisabled(True)
            self.token8high.setDisabled(True)

            self.activatetoken9.setEnabled(False)
            self.tradewithETHtoken9.setEnabled(False)
            self.tradewithERCtoken9.setEnabled(False)
            self.token9ethaddress.setReadOnly(True)
            self.token9low.setReadOnly(True)
            self.token9high.setReadOnly(True)
            self.token9ethaddress.setDisabled(True)
            self.token9low.setDisabled(True)
            self.token9high.setDisabled(True)

            self.activatetoken10.setEnabled(False)
            self.tradewithETHtoken10.setEnabled(False)
            self.tradewithERCtoken10.setEnabled(False)
            self.token10ethaddress.setReadOnly(True)
            self.token10low.setReadOnly(True)
            self.token10high.setReadOnly(True)
            self.token10ethaddress.setDisabled(True)
            self.token10low.setDisabled(True)
            self.token10high.setDisabled(True)
            self.Maxslippage.setDisabled(True)
            self.lineEdit.setDisabled(True)
            self.gweioption.setDisabled(True)
            self.maincoinoption.setDisabled(True)

            self.token1stoploss.setDisabled(True)
            self.token2stoploss.setDisabled(True)
            self.token3stoploss.setDisabled(True)
            self.token4stoploss.setDisabled(True)
            self.token5stoploss.setDisabled(True)
            self.token6stoploss.setDisabled(True)
            self.token7stoploss.setDisabled(True)
            self.token8stoploss.setDisabled(True)
            self.token9stoploss.setDisabled(True)
            self.token10stoploss.setDisabled(True)
            self.token1stoploss.setEnabled(False)
            self.token2stoploss.setEnabled(False)
            self.token3stoploss.setEnabled(False)
            self.token4stoploss.setEnabled(False)
            self.token5stoploss.setEnabled(False)
            self.token6stoploss.setEnabled(False)
            self.token7stoploss.setEnabled(False)
            self.token8stoploss.setEnabled(False)
            self.token9stoploss.setEnabled(False)
            self.token10stoploss.setEnabled(False)

            self.stoplosstoken1.setDisabled(True)
            self.stoplosstoken2.setDisabled(True)
            self.stoplosstoken3.setDisabled(True)
            self.stoplosstoken4.setDisabled(True)
            self.stoplosstoken5.setDisabled(True)
            self.stoplosstoken6.setDisabled(True)
            self.stoplosstoken7.setDisabled(True)
            self.stoplosstoken8.setDisabled(True)
            self.stoplosstoken9.setDisabled(True)
            self.stoplosstoken10.setDisabled(True)
        except Exception as e:
            o = 0

        try:
            if self.activatetoken1.isChecked():
                activatetoken1 = 1
                with open("./configfile.py", "r", encoding="utf-8") as f:
                    poepie = f.read()
                    a = 'activatetoken1='
                    b = '\n'
                    regex = "(?<=%s).*?(?=%s)" % (a, b)
                    lol2 = re.sub(regex, '\'1\'', poepie)
                    f.close()

            else:
                activatetoken1 = 0
                with open("./configfile.py", "r", encoding="utf-8") as f:
                    poepie = f.read()
                    a = 'activatetoken1='
                    b = '\n'
                    regex = "(?<=%s).*?(?=%s)" % (a, b)
                    lol2 = re.sub(regex, '\'0\'', poepie)
                    f.close()
            if self.activatetoken2.isChecked():
                activatetoken2 = 1
                a = 'activatetoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol3 = re.sub(regex, '\'1\'', lol2)
            else:
                activatetoken2 = 0
                a = 'activatetoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol3 = re.sub(regex, '\'0\'', lol2)
            if self.activatetoken3.isChecked():
                activatetoken3 = 1
                a = 'activatetoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol4 = re.sub(regex, '\'1\'', lol3)
            else:
                activatetoken3 = 0
                a = 'activatetoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol4 = re.sub(regex, '\'0\'', lol3)
            if self.activatetoken4.isChecked():
                activatetoken4 = 1
                a = 'activatetoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol5 = re.sub(regex, '\'1\'', lol4)
            else:
                activatetoken4 = 0
                a = 'activatetoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol5 = re.sub(regex, '\'0\'', lol4)
            if self.activatetoken5.isChecked():
                activatetoken5 = 1
                a = 'activatetoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol6 = re.sub(regex, '\'1\'', lol5)
            else:
                activatetoken5 = 0
                a = 'activatetoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol6 = re.sub(regex, '\'0\'', lol5)
            if self.activatetoken6.isChecked():
                activatetoken6 = 1
                a = 'activatetoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol7 = re.sub(regex, '\'1\'', lol6)
            else:
                activatetoken6 = 0
                a = 'activatetoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol7 = re.sub(regex, '\'0\'', lol6)
            if self.activatetoken7.isChecked():
                activatetoken7 = 1
                a = 'activatetoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol8 = re.sub(regex, '\'1\'', lol7)
            else:
                activatetoken7 = 0
                a = 'activatetoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol8 = re.sub(regex, '\'0\'', lol7)
            if self.activatetoken8.isChecked():
                activatetoken8 = 1
                a = 'activatetoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol9 = re.sub(regex, '\'1\'', lol8)
            else:
                activatetoken8 = 0
                a = 'activatetoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol9 = re.sub(regex, '\'0\'', lol8)
            if self.activatetoken9.isChecked():
                activatetoken9 = 1
                a = 'activatetoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol10 = re.sub(regex, '\'1\'', lol9)
            else:
                activatetoken9 = 0
                a = 'activatetoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol10 = re.sub(regex, '\'0\'', lol9)
            if self.activatetoken10.isChecked():
                activatetoken10 = 1
                a = 'activatetoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol11 = re.sub(regex, '\'1\'', lol10)
            else:
                activatetoken10 = 0
                a = 'activatetoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol11 = re.sub(regex, '\'0\'', lol10)
            if self.tradewithETHtoken1.isChecked():
                tradewithETHtoken1 = 1
                a = 'tradewithETHtoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol22 = re.sub(regex, '\'1\'', lol11)
            else:
                tradewithETHtoken1 = 0
                a = 'tradewithETHtoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol22 = re.sub(regex, '\'0\'', lol11)
            if self.tradewithETHtoken2.isChecked():
                tradewithETHtoken2 = 1
                a = 'tradewithETHtoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol23 = re.sub(regex, '\'1\'', lol22)
            else:
                tradewithETHtoken2 = 0
                a = 'tradewithETHtoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol23 = re.sub(regex, '\'0\'', lol22)
            if self.tradewithETHtoken3.isChecked():
                tradewithETHtoken3 = 1
                a = 'tradewithETHtoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol24 = re.sub(regex, '\'1\'', lol23)
            else:
                tradewithETHtoken3 = 0
                a = 'tradewithETHtoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol24 = re.sub(regex, '\'0\'', lol23)
            if self.tradewithETHtoken4.isChecked():
                tradewithETHtoken4 = 1
                a = 'tradewithETHtoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol25 = re.sub(regex, '\'1\'', lol24)
            else:
                tradewithETHtoken4 = 0
                a = 'tradewithETHtoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol25 = re.sub(regex, '\'0\'', lol24)
            if self.tradewithETHtoken5.isChecked():
                tradewithETHtoken5 = 1
                a = 'tradewithETHtoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol26 = re.sub(regex, '\'1\'', lol25)
            else:
                tradewithETHtoken5 = 0
                a = 'tradewithETHtoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol26 = re.sub(regex, '\'0\'', lol25)
            if self.tradewithETHtoken6.isChecked():
                tradewithETHtoken6 = 1
                a = 'tradewithETHtoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol27 = re.sub(regex, '\'1\'', lol26)
            else:
                tradewithETHtoken6 = 0
                a = 'tradewithETHtoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol27 = re.sub(regex, '\'0\'', lol26)
            if self.tradewithETHtoken7.isChecked():
                tradewithETHtoken7 = 1
                a = 'tradewithETHtoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol28 = re.sub(regex, '\'1\'', lol27)
            else:
                tradewithETHtoken7 = 0
                a = 'tradewithETHtoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol28 = re.sub(regex, '\'0\'', lol27)
            if self.tradewithETHtoken8.isChecked():
                tradewithETHtoken8 = 1
                a = 'tradewithETHtoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol29 = re.sub(regex, '\'1\'', lol28)
            else:
                tradewithETHtoken8 = 0
                a = 'tradewithETHtoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol29 = re.sub(regex, '\'0\'', lol28)
            if self.tradewithETHtoken9.isChecked():
                tradewithETHtoken9 = 1
                a = 'tradewithETHtoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol30 = re.sub(regex, '\'1\'', lol29)
            else:
                tradewithETHtoken9 = 0
                a = 'tradewithETHtoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol30 = re.sub(regex, '\'0\'', lol29)
            if self.tradewithETHtoken10.isChecked():
                tradewithETHtoken10 = 1
                a = 'tradewithETHtoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol31 = re.sub(regex, '\'1\'', lol30)
            else:
                tradewithETHtoken10 = 0
                a = 'tradewithETHtoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol31 = re.sub(regex, '\'0\'', lol30)
            if self.tradewithERCtoken1.isChecked():
                tradewithERCtoken1 = 1
                a = 'tradewithERCtoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol32 = re.sub(regex, '\'1\'', lol31)
            else:
                tradewithERCtoken1 = 0
                a = 'tradewithERCtoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol32 = re.sub(regex, '\'0\'', lol31)
            if self.tradewithERCtoken2.isChecked():
                tradewithERCtoken2 = 1
                a = 'tradewithERCtoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol33 = re.sub(regex, '\'1\'', lol32)
            else:
                tradewithERCtoken2 = 0
                a = 'tradewithERCtoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol33 = re.sub(regex, '\'0\'', lol32)
            if self.tradewithERCtoken3.isChecked():
                tradewithERCtoken3 = 1
                a = 'tradewithERCtoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol34 = re.sub(regex, '\'1\'', lol33)
            else:
                tradewithERCtoken3 = 0
                a = 'tradewithERCtoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol34 = re.sub(regex, '\'0\'', lol33)
            if self.tradewithERCtoken4.isChecked():
                tradewithERCtoken4 = 1
                a = 'tradewithERCtoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol35 = re.sub(regex, '\'1\'', lol34)
            else:
                tradewithERCtoken4 = 0
                a = 'tradewithERCtoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol35 = re.sub(regex, '\'0\'', lol34)
            if self.tradewithERCtoken5.isChecked():
                tradewithERCtoken5 = 1
                a = 'tradewithERCtoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol36 = re.sub(regex, '\'1\'', lol35)
            else:
                tradewithERCtoken5 = 0
                a = 'tradewithERCtoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol36 = re.sub(regex, '\'0\'', lol35)
            if self.tradewithERCtoken6.isChecked():
                tradewithERCtoken6 = 1
                a = 'tradewithERCtoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol37 = re.sub(regex, '\'1\'', lol36)
            else:
                tradewithERCtoken6 = 0
                a = 'tradewithERCtoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol37 = re.sub(regex, '\'0\'', lol36)
            if self.tradewithERCtoken7.isChecked():
                tradewithERCtoken7 = 1
                a = 'tradewithERCtoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol38 = re.sub(regex, '\'1\'', lol37)
            else:
                tradewithERCtoken7 = 0
                a = 'tradewithERCtoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol38 = re.sub(regex, '\'0\'', lol37)
            if self.tradewithERCtoken8.isChecked():
                tradewithERCtoken8 = 1
                a = 'tradewithERCtoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol39 = re.sub(regex, '\'1\'', lol38)
            else:
                tradewithERCtoken8 = 0
                a = 'tradewithERCtoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol39 = re.sub(regex, '\'0\'', lol38)
            if self.tradewithERCtoken9.isChecked():
                tradewithERCtoken9 = 1
                a = 'tradewithERCtoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol40 = re.sub(regex, '\'1\'', lol39)
            else:
                tradewithERCtoken9 = 0
                a = 'tradewithERCtoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol40 = re.sub(regex, '\'0\'', lol39)
            if self.tradewithERCtoken10.isChecked():
                tradewithERCtoken10 = 1
                a = 'tradewithERCtoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol41 = re.sub(regex, '\'1\'', lol40)
            else:
                tradewithERCtoken10 = 0
                a = 'tradewithERCtoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol41 = re.sub(regex, '\'0\'', lol40)

            token1low = self.token1low.text()
            a = 'token1low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol42 = re.sub(regex, '\'' + str(token1low) + '\'', lol41)
            token2low = self.token2low.text()
            a = 'token2low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol43 = re.sub(regex, '\'' + str(token2low) + '\'', lol42)
            token3low = self.token3low.text()
            a = 'token3low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol44 = re.sub(regex, '\'' + str(token3low) + '\'', lol43)
            token4low = self.token4low.text()
            a = 'token4low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol45 = re.sub(regex, '\'' + str(token4low) + '\'', lol44)
            token5low = self.token5low.text()
            a = 'token5low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol46 = re.sub(regex, '\'' + str(token5low) + '\'', lol45)
            token6low = self.token6low.text()
            a = 'token6low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol47 = re.sub(regex, '\'' + str(token6low) + '\'', lol46)
            token7low = self.token7low.text()
            a = 'token7low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol48 = re.sub(regex, '\'' + str(token7low) + '\'', lol47)
            token8low = self.token8low.text()
            a = 'token8low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol49 = re.sub(regex, '\'' + str(token8low) + '\'', lol48)
            token9low = self.token9low.text()
            a = 'token9low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol50 = re.sub(regex, '\'' + str(token9low) + '\'', lol49)
            token10low = self.token10low.text()
            a = 'token10low='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol51 = re.sub(regex, '\'' + str(token10low) + '\'', lol50)
            token1high = self.token1high.text()
            a = 'token1high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol52 = re.sub(regex, '\'' + str(token1high) + '\'', lol51)
            token2high = self.token2high.text()
            a = 'token2high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol53 = re.sub(regex, '\'' + str(token2high) + '\'', lol52)
            token3high = self.token3high.text()
            a = 'token3high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol54 = re.sub(regex, '\'' + str(token3high) + '\'', lol53)
            token4high = self.token4high.text()
            a = 'token4high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol55 = re.sub(regex, '\'' + str(token4high) + '\'', lol54)
            token5high = self.token5high.text()
            a = 'token5high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol56 = re.sub(regex, '\'' + str(token5high) + '\'', lol55)
            token6high = self.token6high.text()
            a = 'token6high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol57 = re.sub(regex, '\'' + str(token6high) + '\'', lol56)
            token7high = self.token7high.text()
            a = 'token7high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol58 = re.sub(regex, '\'' + str(token7high) + '\'', lol57)
            token8high = self.token8high.text()
            a = 'token8high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol59 = re.sub(regex, '\'' + str(token8high) + '\'', lol58)
            token9high = self.token9high.text()
            a = 'token9high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol60 = re.sub(regex, '\'' + str(token9high) + '\'', lol59)
            token10high = self.token10high.text()
            a = 'token10high='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol61 = re.sub(regex, '\'' + str(token10high) + '\'', lol60)
            token1ethaddress = self.token1ethaddress.text()
            a = 'token1ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol62 = re.sub(regex, '\'' + str(token1ethaddress) + '\'', lol61)
            token2ethaddress = self.token2ethaddress.text()
            a = 'token2ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol63 = re.sub(regex, '\'' + str(token2ethaddress) + '\'', lol62)
            token3ethaddress = self.token3ethaddress.text()
            a = 'token3ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol64 = re.sub(regex, '\'' + str(token3ethaddress) + '\'', lol63)
            token4ethaddress = self.token4ethaddress.text()
            a = 'token4ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol65 = re.sub(regex, '\'' + str(token4ethaddress) + '\'', lol64)
            token5ethaddress = self.token5ethaddress.text()
            a = 'token5ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol66 = re.sub(regex, '\'' + str(token5ethaddress) + '\'', lol65)
            token6ethaddress = self.token6ethaddress.text()
            a = 'token6ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol67 = re.sub(regex, '\'' + str(token6ethaddress) + '\'', lol66)
            token7ethaddress = self.token7ethaddress.text()
            a = 'token7ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol68 = re.sub(regex, '\'' + str(token7ethaddress) + '\'', lol67)
            token8ethaddress = self.token8ethaddress.text()
            a = 'token8ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol69 = re.sub(regex, '\'' + str(token8ethaddress) + '\'', lol68)
            token9ethaddress = self.token9ethaddress.text()
            a = 'token9ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol70 = re.sub(regex, '\'' + str(token9ethaddress) + '\'', lol69)
            token10ethaddress = self.token10ethaddress.text()
            a = 'token10ethaddress='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol71 = re.sub(regex, '\'' + str(token10ethaddress) + '\'', lol70)
            infuraurl = self.infuraurl.text()
            a = 'infuraurl='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol72 = re.sub(regex, '\'' + str(infuraurl) + '\'', lol71)
            tokentokennumerator = self.tokentokennumerator.text()
            a = 'tokentokennumerator='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol73 = re.sub(regex, '\'' + str(tokentokennumerator) + '\'', lol72)
            secondscheckingprice = self.secondscheckingprice.value()
            a = 'secondscheckingprice='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol74 = re.sub(regex, '\'' + str(secondscheckingprice) + '\'', lol73)
            secondswaitaftertrade = self.secondscheckingprice_2.value()
            a = 'secondswaitaftertrade='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol75 = re.sub(regex, '\'' + str(secondswaitaftertrade) + '\'', lol74)
            secondscheckingprice_2 = self.secondscheckingprice_2.value()
            a = 'secondscheckingprice_2='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol76 = re.sub(regex, '\'' + str(secondscheckingprice_2) + '\'', lol75)
            lol77 = re.sub('\'\'', '\'0\'', lol76)
            token1name = self.token1name.text()
            a = 'token1name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol78 = re.sub(regex, '\'' + str(token1name) + '\'', lol77)
            token2name = self.token2name.text()
            a = 'token2name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol79 = re.sub(regex, '\'' + str(token2name) + '\'', lol78)
            token3name = self.token3name.text()
            a = 'token3name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol80 = re.sub(regex, '\'' + str(token3name) + '\'', lol79)
            token4name = self.token4name.text()
            a = 'token4name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol81 = re.sub(regex, '\'' + str(token4name) + '\'', lol80)
            token5name = self.token5name.text()
            a = 'token5name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol82 = re.sub(regex, '\'' + str(token5name) + '\'', lol81)
            token6name = self.token6name.text()
            a = 'token6name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol83 = re.sub(regex, '\'' + str(token6name) + '\'', lol82)
            token7name = self.token7name.text()
            a = 'token7name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol84 = re.sub(regex, '\'' + str(token7name) + '\'', lol83)
            token8name = self.token8name.text()
            a = 'token8name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol85 = re.sub(regex, '\'' + str(token8name) + '\'', lol84)
            token9name = self.token9name.text()
            a = 'token9name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol86 = re.sub(regex, '\'' + str(token9name) + '\'', lol85)
            token10name = self.token10name.text()
            a = 'token10name='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol87 = re.sub(regex, '\'' + str(token10name) + '\'', lol86)
            maxslippage = self.Maxslippage.text()
            a = 'max_slippage='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol88 = re.sub(regex, '\'' + str(maxslippage) + '\'', lol87)
            ethtokeep = self.lineEdit.text()
            a = 'ethtokeep='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol89 = re.sub(regex, '\'' + str(ethtokeep) + '\'', lol88)
            a = 'speed='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol90 = re.sub(regex, '\'' + str(speed) + '\'', lol89)
            a = 'maincoinoption='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol91 = re.sub(regex, '\'' + str(maincoinoption) + '\'', lol90)
            lol92 = re.sub('\'\'', '\'0\'', lol91)

            if self.stoplosstoken1.isChecked():
                stoplosstoken1 = 1
                a = 'stoplosstoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol93 = re.sub(regex, '\'1\'', lol92)
            else:
                stoplosstoken1 = 0
                a = 'stoplosstoken1='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol93 = re.sub(regex, '\'0\'', lol92)
            if self.stoplosstoken2.isChecked():
                stoplosstoken2 = 1
                a = 'stoplosstoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol94 = re.sub(regex, '\'1\'', lol93)
            else:
                stoplosstoken2 = 0
                a = 'stoplosstoken2='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol94 = re.sub(regex, '\'0\'', lol93)
            if self.stoplosstoken3.isChecked():
                stoplosstoken3 = 1
                a = 'stoplosstoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol95 = re.sub(regex, '\'1\'', lol94)
            else:
                stoplosstoken3 = 0
                a = 'stoplosstoken3='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol95 = re.sub(regex, '\'0\'', lol94)
            if self.stoplosstoken4.isChecked():
                stoplosstoken4 = 1
                a = 'stoplosstoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol96 = re.sub(regex, '\'1\'', lol95)
            else:
                stoplosstoken4 = 0
                a = 'stoplosstoken4='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol96 = re.sub(regex, '\'0\'', lol95)
            if self.stoplosstoken5.isChecked():
                stoplosstoken5 = 1
                a = 'stoplosstoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol97 = re.sub(regex, '\'1\'', lol96)
            else:
                stoplosstoken5 = 0
                a = 'stoplosstoken5='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol97 = re.sub(regex, '\'0\'', lol96)
            if self.stoplosstoken6.isChecked():
                stoplosstoken6 = 1
                a = 'stoplosstoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol98 = re.sub(regex, '\'1\'', lol97)
            else:
                stoplosstoken6 = 0
                a = 'stoplosstoken6='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol98 = re.sub(regex, '\'0\'', lol97)
            if self.stoplosstoken7.isChecked():
                stoplosstoken7 = 1
                a = 'stoplosstoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol99 = re.sub(regex, '\'1\'', lol98)
            else:
                stoplosstoken7 = 0
                a = 'stoplosstoken7='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol99 = re.sub(regex, '\'0\'', lol98)
            if self.stoplosstoken8.isChecked():
                stoplosstoken8 = 1
                a = 'stoplosstoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol100 = re.sub(regex, '\'1\'', lol99)
            else:
                stoplosstoken8 = 0
                a = 'stoplosstoken8='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol100 = re.sub(regex, '\'0\'', lol99)
            if self.stoplosstoken9.isChecked():
                stoplosstoken9 = 1
                a = 'stoplosstoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol101 = re.sub(regex, '\'1\'', lol100)
            else:
                stoplosstoken9 = 0
                a = 'stoplosstoken9='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol101 = re.sub(regex, '\'0\'', lol100)
            if self.stoplosstoken10.isChecked():
                stoplosstoken10 = 1
                a = 'stoplosstoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol102 = re.sub(regex, '\'1\'', lol101)
            else:
                stoplosstoken10 = 0
                a = 'stoplosstoken10='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol102 = re.sub(regex, '\'0\'', lol101)

            token1stoploss = self.token1stoploss.text()
            a = 'token1stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol103 = re.sub(regex, '\'' + str(token1stoploss) + '\'', lol102)
            token2stoploss = self.token2stoploss.text()
            a = 'token2stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol104 = re.sub(regex, '\'' + str(token2stoploss) + '\'', lol103)
            token3stoploss = self.token3stoploss.text()
            a = 'token3stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol105 = re.sub(regex, '\'' + str(token3stoploss) + '\'', lol104)
            token4stoploss = self.token4stoploss.text()
            a = 'token4stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol106 = re.sub(regex, '\'' + str(token4stoploss) + '\'', lol105)
            token5stoploss = self.token5stoploss.text()
            a = 'token5stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol107 = re.sub(regex, '\'' + str(token5stoploss) + '\'', lol106)
            token6stoploss = self.token6stoploss.text()
            a = 'token6stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol108 = re.sub(regex, '\'' + str(token6stoploss) + '\'', lol107)
            token7stoploss = self.token7stoploss.text()
            a = 'token7stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol109 = re.sub(regex, '\'' + str(token7stoploss) + '\'', lol108)
            token8stoploss = self.token8stoploss.text()
            a = 'token8stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol110 = re.sub(regex, '\'' + str(token8stoploss) + '\'', lol109)
            token9stoploss = self.token9stoploss.text()
            a = 'token9stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol111 = re.sub(regex, '\'' + str(token9stoploss) + '\'', lol110)
            token10stoploss = self.token10stoploss.text()
            a = 'token10stoploss='
            b = '\n'
            regex = "(?<=%s).*?(?=%s)" % (a, b)
            lol112 = re.sub(regex, '\'' + str(token10stoploss) + '\'', lol111)

            if self.debugmode.isChecked():
                debugmode = 1
                a = 'debugmode='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol113 = re.sub(regex, '\'1\'', lol112)
            else:
                debugmode = 0
                a = 'debugmode='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol113 = re.sub(regex, '\'0\'', lol112)
            
            if self.maxgwei.isChecked():
                maxgwei = 1
                a = 'maxgwei='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol114 = re.sub(regex, '\'1\'', lol113)
            else:
                maxgwei = 0
                a = 'maxgwei='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol114 = re.sub(regex, '\'0\'', lol113)
                
            if self.diffdeposit.isChecked():
                diffdeposit = 1
                a = 'diffdeposit='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol115 = re.sub(regex, '\'1\'', lol114)
            else:
                diffdeposit = 0
                a = 'diffdeposit='
                b = '\n'
                regex = "(?<=%s).*?(?=%s)" % (a, b)
                lol115 = re.sub(regex, '\'0\'', lol114)

            with open("./configfile.py", "w", encoding="utf-8") as f:
                f.write(lol115)
                f.close()
        except Exception as e:
            o = 0
        self.log.append('starting {} threads'.format(self.NUM_THREADS))
        self.startbutton.setDisabled(True)
        self.stopbutton.setEnabled(True)

        self.__workers_done = 0
        self.__threads = []
        for idx in range(self.NUM_THREADS):
            worker = Worker(idx)
            thread = QThread()
            thread.setObjectName('thread_' + str(idx))
            self.__threads.append((thread, worker))  # need to store worker too otherwise will be gc'd
            worker.moveToThread(thread)

            # get progress messages from worker:
            worker.sig_step.connect(self.on_worker_step)
            worker.sig_done.connect(self.on_worker_done)
            worker.sig_msg.connect(self.log.append)

            # control worker:
            self.sig_abort_workers.connect(worker.abort)

            # get read to start worker:
            # self.sig_start.connect(worker.work)  # needed due to PyCharm debugger bug (!); comment out next line

            thread.started.connect(worker.work)
            thread.start()  # this will emit 'started' and start thread's event loop
        # self.sig_start.emit()  # needed due to PyCharm debugger bug (!)

    @pyqtSlot(int, str)
    def on_worker_step(self, worker_id: int, data: str):
        self.log.append('Worker #{}: {}'.format(worker_id, data))
        self.progress.append('{}: {}'.format(worker_id, data))

    @pyqtSlot(int)
    def on_worker_done(self, worker_id):
        self.log.append('worker #{} done'.format(worker_id))
        self.progress.append('-- Worker {} DONE'.format(worker_id))
        self.__workers_done += 1
        if self.__workers_done == self.NUM_THREADS:
            self.log.append('No more workers active')
            self.startbutton.setEnabled(True)
            self.stopbutton.setDisabled(True)
            # self.__threads = None


    @pyqtSlot()
    def abort_workers(self):
        self.startbutton.setDisabled(True)
        self.stopbutton.setDisabled(True)
        self.sig_abort_workers.emit()
        self.log.append('Asking each worker to abort')
        for thread, worker in self.__threads:  # note nice unpacking by Python, avoids indexing
            thread.quit()  # this will quit **as soon as thread event loop unblocks**
            print('Stopping bot (takes 15 seconds)')
            thread.wait()  # <- so you need to wait for it to *actually* quit

        # even though threads have exited, there may still be messages on the main thread's
        # queue (messages that threads emitted before the abort):
        self.log.append('All threads exited')



        def lol2():
            self.startbutton.setEnabled(True)
            self.stopbutton.setDisabled(True)
            try:
                self.secondscheckingprice_2.setEnabled(True)
                self.secondscheckingprice.setEnabled(True)
                self.infuraurl.setEnabled(True)
                self.tokentokennumerator.setEnabled(True)
                self.activatetoken1.setEnabled(True)
                self.tradewithETHtoken1.setEnabled(True)
                self.tradewithERCtoken1.setEnabled(True)
                self.token1ethaddress.setReadOnly(False)
                self.token1low.setReadOnly(False)
                self.token1high.setReadOnly(False)
                self.token1ethaddress.setEnabled(True)
                self.token1low.setEnabled(True)
                self.token1high.setEnabled(True)

                self.gweioption.setEnabled(True)
                self.maincoinoption.setEnabled(True)

                self.activatetoken2.setEnabled(True)
                self.tradewithETHtoken2.setEnabled(True)
                self.tradewithERCtoken2.setEnabled(True)
                self.token2ethaddress.setReadOnly(False)
                self.token2low.setReadOnly(False)
                self.token2high.setReadOnly(False)
                self.token2ethaddress.setEnabled(True)
                self.token2low.setEnabled(True)
                self.token2high.setEnabled(True)

                self.activatetoken3.setEnabled(True)
                self.tradewithETHtoken3.setEnabled(True)
                self.tradewithERCtoken3.setEnabled(True)
                self.token3ethaddress.setReadOnly(False)
                self.token3low.setReadOnly(False)
                self.token3high.setReadOnly(False)
                self.token3ethaddress.setEnabled(True)
                self.token3low.setEnabled(True)
                self.token3high.setEnabled(True)

                self.updatename.setEnabled(True)

                self.activatetoken4.setEnabled(True)
                self.tradewithETHtoken4.setEnabled(True)
                self.tradewithERCtoken4.setEnabled(True)
                self.token4ethaddress.setReadOnly(False)
                self.token4low.setReadOnly(False)
                self.token4high.setReadOnly(False)
                self.token4ethaddress.setEnabled(True)
                self.token4low.setEnabled(True)
                self.token4high.setEnabled(True)

                self.activatetoken5.setEnabled(True)
                self.tradewithETHtoken5.setEnabled(True)
                self.tradewithERCtoken5.setEnabled(True)
                self.token5ethaddress.setReadOnly(False)
                self.token5low.setReadOnly(False)
                self.token5high.setReadOnly(False)
                self.token5ethaddress.setEnabled(True)
                self.token5low.setEnabled(True)
                self.token5high.setEnabled(True)

                self.activatetoken6.setEnabled(True)
                self.tradewithETHtoken6.setEnabled(True)
                self.tradewithERCtoken6.setEnabled(True)
                self.token6ethaddress.setReadOnly(False)
                self.token6low.setReadOnly(False)
                self.token6high.setReadOnly(False)
                self.token6ethaddress.setEnabled(True)
                self.token6low.setEnabled(True)
                self.token6high.setEnabled(True)

                self.activatetoken7.setEnabled(True)
                self.tradewithETHtoken7.setEnabled(True)
                self.tradewithERCtoken7.setEnabled(True)
                self.token7ethaddress.setReadOnly(False)
                self.token7low.setReadOnly(False)
                self.token7high.setReadOnly(False)
                self.token7ethaddress.setEnabled(True)
                self.token7low.setEnabled(True)
                self.token7high.setEnabled(True)

                self.activatetoken8.setEnabled(True)
                self.tradewithETHtoken8.setEnabled(True)
                self.tradewithERCtoken8.setEnabled(True)
                self.token8ethaddress.setReadOnly(False)
                self.token8low.setReadOnly(False)
                self.token8high.setReadOnly(False)
                self.token8ethaddress.setEnabled(True)
                self.token8low.setEnabled(True)
                self.token8high.setEnabled(True)

                self.activatetoken9.setEnabled(True)
                self.tradewithETHtoken9.setEnabled(True)
                self.tradewithERCtoken9.setEnabled(True)
                self.token9ethaddress.setReadOnly(False)
                self.token9low.setReadOnly(False)
                self.token9high.setReadOnly(False)
                self.token9ethaddress.setEnabled(True)
                self.token9low.setEnabled(True)
                self.token9high.setEnabled(True)

                self.activatetoken10.setEnabled(True)
                self.tradewithETHtoken10.setEnabled(True)
                self.tradewithERCtoken10.setEnabled(True)
                self.token10ethaddress.setReadOnly(False)
                self.token10low.setReadOnly(False)
                self.token10high.setReadOnly(False)
                self.token10ethaddress.setEnabled(True)
                self.token10low.setEnabled(True)
                self.token10high.setEnabled(True)
                self.Maxslippage.setEnabled(True)
                self.lineEdit.setEnabled(True)

                self.token1stoploss.setEnabled(True)
                self.token2stoploss.setEnabled(True)
                self.token3stoploss.setEnabled(True)
                self.token4stoploss.setEnabled(True)
                self.token5stoploss.setEnabled(True)
                self.token6stoploss.setEnabled(True)
                self.token7stoploss.setEnabled(True)
                self.token8stoploss.setEnabled(True)
                self.token9stoploss.setEnabled(True)
                self.token10stoploss.setEnabled(True)

                self.stoplosstoken1.setEnabled(True)
                self.stoplosstoken2.setEnabled(True)
                self.stoplosstoken3.setEnabled(True)
                self.stoplosstoken4.setEnabled(True)
                self.stoplosstoken5.setEnabled(True)
                self.stoplosstoken6.setEnabled(True)
                self.stoplosstoken7.setEnabled(True)
                self.stoplosstoken8.setEnabled(True)
                self.stoplosstoken9.setEnabled(True)
                self.stoplosstoken10.setEnabled(True)
                self.debugmode.setEnabled(True)
                self.maxgwei.setEnabled(True)
                self.diffdeposit.setEnabled(True)
                self.maxgweinumber.setReadOnly(False)
                self.diffdepositaddress.setReadOnly(False)
                self.maxgweinumber.setEnabled(True)
                self.diffdepositaddress.setEnabled(True)
            except Exception as e:
                o = 0
        print('Bot stopped')
        lol2()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    lollol = ui.setupUi(MainWindow)
    lollol2 = MainWindow.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        o = 0
    print(lollol2)