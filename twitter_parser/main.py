import asyncio
import time
import argparse
from twikit import Client
from itertools import count
from config import COUNT
from process_data import save_tweets

parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="name of the company ticker")
args = parser.parse_args()

TICKER = args.ticker
QUERY = f'"{TICKER}" (from:davidfaber OR from:Kellblog OR from:PhilipEtienne OR from:awealthofcs OR from:MorningstarInc OR from:ValueDude OR from:MicroFundy OR from:Forbes OR from:LizAnnSonders OR from:FT OR from:DumbLuckCapital OR from:BergenCapital OR from:probesreporter OR from:GRDecter OR from:michaelbatnick OR from:BluegrassCap OR from:davidein OR from:stlouisfed OR from:CNBC OR from:chamath OR from:HedgeyeENERGY OR from:GoldmanSachs OR from:JacobWolinsky OR from:paulkrugman OR from:GlaucusResearch OR from:WSJ OR from:AswathDamodaran OR from:matt_levine OR from:michaelkitces OR from:SallieKrawcheck OR from:OnlyCFO OR from:EdBorgato OR from:TigreCapital OR from:JohnHuber72 OR from:TruthGundlach OR from:firstadopter OR from:footnoted OR from:QTRResearch OR from:realDonaldTrump OR from:LongShortTrader OR from:xuexishenghuo OR from:marginalidea OR from:AZ_Value OR from:AlderLaneeggs OR from:dailydirtnap OR from:herbgreenberg OR from:ActAccordingly OR from:FatTailCapital OR from:LibertyRPF OR from:cullenroche OR from:BarbarianCap OR from:TheStalwart OR from:sprucepointcap OR from:BlackRock OR from:jessefelder OR from:ErikFossing OR from:pmarca OR from:AureliusValue OR from:business OR from:IanShepherdson OR from:John_Hempton OR from:MorganStanley OR from:zerohedge OR from:ReformedBroker OR from:ShortSightedCap OR from:WSJmarkets OR from:Hedge_FundGirl OR from:felixsalmon OR from:modestproposal1 OR from:PlanMaestro OR from:fundiescapital OR from:RayDalio OR from:mattturck OR from:Jesse_Livermore OR from:mjmauboussin OR from:jasonzweigwsj OR from:valuewalk OR from:bespokeinvest OR from:Cokedupoptions OR from:JustinWolfers OR from:jay_21_ OR from:TheEconomist OR from:muddywatersre OR from:ritholtz OR from:manualofideas OR from:Find_Me_Value OR from:FundyLongShort OR from:Nouriel OR from:UnionSquareGrp OR from:GrantsPub OR from:plainview_ OR from:EventDrivenMgr OR from:UnderwaterCap OR from:KerrisdaleCap OR from:GothamResearch OR from:AlexRubalcava OR from:gkm1 OR from:CitronResearch OR from:CopperfieldRscr OR from:PresciencePoint OR from:schaudenfraud OR from:nytimesbusiness OR from:Carl_C_Icahn OR from:marketfolly OR from:unusual_whales) -filter:replies'

client = Client('en-US')

def is_tweets(tweets):
    """
    Проверка на наличие твитов.
    """
    if not tweets:
        print('Tweets not found')
        return False
    return True

async def main():
    client.load_cookies('cookies.json')
    
    tweets = await client.search_tweet(query=QUERY,
                                       product='Latest',
                                       count=COUNT)
    
    counter = count()
    
    while is_tweets(tweets):
        counter = save_tweets(tweets, counter, TICKER)
        time.sleep(5)
        try:
            tweets = await tweets.next()
        except Exception as e:
            print(e)
            break
    
    print(f'Collected {next(counter)} tweets')
    

asyncio.run(main())
