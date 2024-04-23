# Given two newspapers returns the simils articles with name and links
import multiprocessing
from multiprocessing import Process
from utils import extract_articles, calculate_nlp, calculate_similarity
from multiprocessing import Pool

# python3 -m spacy download en_core_web_trf

DAY = "2024-04-20"
START_TIME = "08:00:00"
END_TIME = "12:59:59"

BASE_DIR = "../../Newscraping/collectedNews/flow"
NEWSPAPER_A = "EN/RioTimes"
NEWSPAPER_B = "EN/NewsComAu"
COSINE_THRESHOLD = 0.98

"""
Australia’s Indigenous Doubt Impact of Rights Vote - https://www.riotimesonline.com/australias-indigenous-doubt-impact-of-rights-vote/ - Ten-year-old Indigenous boy takes own life in state care, suicide prevention body says - https://www.news.com.au/lifestyle/health/mental-health/tenyearold-indigenous-boy-takes-own-life-in-state-care-suicide-prevention-body-says/news-story/85d03ee10b7574196d3ad3f27d82b7b1?from=rss-basic - 0.9840738542590833
Australia’s Indigenous Doubt Impact of Rights Vote - https://www.riotimesonline.com/australias-indigenous-doubt-impact-of-rights-vote/ - 3 per cent of Gen Z and Millennials think politicians have their interests at heart, seeing them as ‘selfish’ and ‘corrupt’ - https://www.news.com.au/finance/economy/australian-economy/just-three-per-cent-of-gen-z-and-millennials-think-politicians-have-their-interests-at-heart-seeing-them-as-selfish-and-corrupt/news-story/50b2a2a71ec5a4a5fa026b7e317c8fe1?from=rss-basic - 0.9803423722817282
Pakistan launches airstrikes against Iran: A Tale of Retaliation and Resistance - https://www.riotimesonline.com/pakistan-launches-airstrikes-against-iran-a-tale-of-retaliation-and-resistance/ - Pro-Palestine activists promise ‘economic pain’, across Aussie cities in chaotic protest action - https://www.news.com.au/world/middle-east/propalestine-activists-promise-economic-pain-across-aussie-cities-in-chaotic-protest-action/news-story/dd4590481b8cfed427d9a99b5fdcae1e?from=rss-basic - 0.982238632503867
Europe’s Magnesium Revival: Securing Strategic Autonomy - https://www.riotimesonline.com/europes-magnesium-revival-securing-strategic-autonomy/ - Anthony Albanese unveils millions for critical minerals projects to fend off Chinese supply chokehold - https://www.news.com.au/national/politics/anthony-albanese-unveils-millions-for-critical-minerals-projects-to-fend-off-chinese-supply-chokehold/news-story/4c5a2336f9f55aac26bc8361c94dd07a?from=rss-basic - 0.9827059364811042
Japan’s $67 Billion Bid for Chip Leadership - https://www.riotimesonline.com/japans-67-billion-bid-for-chip-leadership/ - Anthony Albanese unveils millions for critical minerals projects to fend off Chinese supply chokehold - https://www.news.com.au/national/politics/anthony-albanese-unveils-millions-for-critical-minerals-projects-to-fend-off-chinese-supply-chokehold/news-story/4c5a2336f9f55aac26bc8361c94dd07a?from=rss-basic - 0.9805711723801476
Yen’s Historic Decline Triggers Intervention Speculation - https://www.riotimesonline.com/yens-historic-decline-triggers-intervention-speculation/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9802624874246382
Zimbabwe Launches Gold-Backed ZiG Currency in Economic Revamp - https://www.riotimesonline.com/zimbabwe-launches-gold-backed-zig-currency-in-economic-revamp/ - Anthony Albanese unveils millions for critical minerals projects to fend off Chinese supply chokehold - https://www.news.com.au/national/politics/anthony-albanese-unveils-millions-for-critical-minerals-projects-to-fend-off-chinese-supply-chokehold/news-story/4c5a2336f9f55aac26bc8361c94dd07a?from=rss-basic - 0.9813946570976098
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - Pro-Palestine activists promise ‘economic pain’, across Aussie cities in chaotic protest action - https://www.news.com.au/world/middle-east/propalestine-activists-promise-economic-pain-across-aussie-cities-in-chaotic-protest-action/news-story/dd4590481b8cfed427d9a99b5fdcae1e?from=rss-basic - 0.9826043189233739
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - Prime Minister leads condemnation of Iranian attacks on Israel as additional military support rejected - https://www.news.com.au/world/middle-east/labor-coalition-condemn-iranian-attacks-on-israel-as-albanese-government-rejects-additional-military-support/news-story/82d2cd86acfe4c85a0fe67ef314e87ff?from=rss-basic - 0.983450680399663
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - Map reveals shock reality of crisis after Iran attacked Israel - https://www.news.com.au/technology/innovation/military/the-moment-the-whole-world-has-feared-leaders-condemn-irans-strike-on-israel/news-story/f7dd1fc6960c914a01f765883b454f64?from=rss-basic - 0.9824256406472996
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - US, UK militaries shoot down Iranian drones launched at Israel - https://www.news.com.au/technology/innovation/military/iran-launches-drone-attack-on-israel-america-vows-to-support-its-allys-defense-against-tehran/news-story/e77b1ab135dadc66428a19937c922310?from=rss-basic - 0.98440076695334
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - Big Qantas call as world prepares for attack - https://www.news.com.au/technology/innovation/military/sooner-than-later-global-conflict-warnings-as-israel-braces-for-attack-from-iran/news-story/ff7cfdf85339596744e1eab597c03ab2?from=rss-basic - 0.9823690919117383
New Military Operation in Nagorno-Karabakh Reignites Tensions - https://www.riotimesonline.com/new-military-operation-in-nagorno-karabakh-reignites-tensions/ - ‘Leave’: Aussies told to evacuate Israel after nation launched a missile attack in retaliation at Iran - https://www.news.com.au/world/middle-east/israel-launches-missile-strike-against-iran/news-story/85cfbc13bc2ce1e2a92f2835f1b99bfc?from=rss-basic - 0.9801274100827786
Asian Currencies Hit Lows Amid Economic Slump - https://www.riotimesonline.com/asian-currencies-hit-lows-amid-economic-slump/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9803475948384072
Paris 2024 Olympics: Enhanced Security Amid Growing Islamist Terrorism Concerns - https://www.riotimesonline.com/paris-2024-olympics-enhanced-security-amid-growing-islamist-terrorism-concerns/ - Tourists blamed for ruining major attraction in Hawaii - https://www.news.com.au/travel/travel-updates/warnings/tourists-blamed-for-ruining-major-attraction-in-hawaii/news-story/00e64b901966c7e27578b059f682de41?from=rss-basic - 0.9803152660647274
Saudi Arabia Eyes African Minerals for Energy Shift - https://www.riotimesonline.com/saudi-arabia-eyes-african-minerals-for-energy-shift/ - Anthony Albanese unveils millions for critical minerals projects to fend off Chinese supply chokehold - https://www.news.com.au/national/politics/anthony-albanese-unveils-millions-for-critical-minerals-projects-to-fend-off-chinese-supply-chokehold/news-story/4c5a2336f9f55aac26bc8361c94dd07a?from=rss-basic - 0.9842819951501391
Escalating Tensions: U.S., Israel, and Iran on the Brink - https://www.riotimesonline.com/escalating-tensions-u-s-israel-and-iran-on-the-brink/ - ‘Critical next few hours’: What we know about Israel’s retaliatory strike on Iran - https://www.news.com.au/world/middle-east/critical-next-few-hours-what-we-know-about-israels-retaliatory-strike-on-iran/news-story/48afe1902c256508b717da70ec5dd0aa?from=rss-basic - 0.9807231771479784
UBS Predicts Potential Fed Rate Hike to 6.5% - https://www.riotimesonline.com/ubs-predicts-potential-fed-rate-hike-to-6-5/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9831923888130653
President Biden’s Diplomatic Strategy on Iran-Israel Conflict - https://www.riotimesonline.com/president-bidens-diplomatic-strategy-on-iran-israel-conflict/ - US, UK militaries shoot down Iranian drones launched at Israel - https://www.news.com.au/technology/innovation/military/iran-launches-drone-attack-on-israel-america-vows-to-support-its-allys-defense-against-tehran/news-story/e77b1ab135dadc66428a19937c922310?from=rss-basic - 0.9824287150332067
President Biden’s Diplomatic Strategy on Iran-Israel Conflict - https://www.riotimesonline.com/president-bidens-diplomatic-strategy-on-iran-israel-conflict/ - Big Qantas call as world prepares for attack - https://www.news.com.au/technology/innovation/military/sooner-than-later-global-conflict-warnings-as-israel-braces-for-attack-from-iran/news-story/ff7cfdf85339596744e1eab597c03ab2?from=rss-basic - 0.9820174116665222
Trump’s Trial Begins Amid Claims of Political Persecution - https://www.riotimesonline.com/trumps-trial-begins-amid-claims-of-political-persecution/ - Tuhirangi-Thomas Tahiata fails to overturn convictions for horrific 2016 toolbox murders of Cory Breton, Iuliana Triscaru - https://www.news.com.au/national/queensland/courts-law/tuhirangithomas-tahiata-fails-to-overturn-convictions-for-horrific-2016-toolbox-murders-of-cory-breton-iuliana-triscaru/news-story/ff873f2f6eb3229240f66003ac724840?from=rss-basic - 0.9810341321219906
Fed Hints at Delayed Rate Cuts Amid Inflation Challenges - https://www.riotimesonline.com/fed-hints-at-delayed-rate-cuts-amid-inflation-challenges/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9859557783031432
Rising Debt Amid Push for Increased Spending in Brazil - https://www.riotimesonline.com/rising-debt-amid-push-for-increased-spending-in-brazil/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9821443725136685
Inter Secures Victory Over Palmeiras with Perfect Record Intact - https://www.riotimesonline.com/inter-secures-victory-over-palmeiras-with-perfect-record-intact/ - Goal-shy Olyroos to ‘regret’ not selecting Bayern Munich-bound teenager Nestory Irankunda - https://www.news.com.au/sport/football/goalshy-olyroos-reeling-after-shock-10-loss-to-indonesia/news-story/82ad562934206279e24e6a8ce4b6e514?from=rss-basic - 0.9813437853947473
2024 Bight Be The Year Bitcoin and Co. May Overcome Their Reputation Issue - https://www.riotimesonline.com/2024-bight-be-the-year-bitcoin-and-co-may-overcome-their-reputation-issue/ - Cryptocurrency world braces for bitcoin ‘halving’ event - https://www.news.com.au/finance/money/costs/cryptocurrency-world-braces-for-bitcoin-halving-event/news-story/ce84781d55fae75171f89be5e89f2075?from=rss-basic - 0.9877065461663442
Continued Investor Caution Amid Fiscal Risks Impacts Brazilian Shares - https://www.riotimesonline.com/continued-investor-caution-amid-fiscal-risks-impacts-brazilian-shares/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9808680762470565
Dollar Retreats Following Brazilian Central Bank Remarks - https://www.riotimesonline.com/u-s-dollar-experiences-decline-amid-brazils-central-bank-stance/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9822878312390896
Ibovespa Ekes Out Minor Gain, Halting Seven-Day Losing Streak - https://www.riotimesonline.com/ibovespa-ekes-out-minor-gain-halting-seven-day-losing-streak/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9864542681215057
Dollar Falls 1% Amid Market Adjustments Despite Weekly Gain - https://www.riotimesonline.com/dollar-falls-1-amid-market-adjustments-despite-weekly-gain/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9807766152955706
Belize – One of Latin America’s Best-Kept Secrets - https://www.riotimesonline.com/belize-one-of-latin-americas-best-kept-secrets/ - As a first time motorhome traveller, this is why it’s booming on the roads of Australia - https://www.news.com.au/travel/travel-ideas/road-trips/as-a-first-time-motorhome-traveller-this-is-why-its-booming-on-the-roads-of-australia/news-story/5da26b5758d3de0c57e2008971f41ce9?from=rss-basic - 0.9803165378189814
Argentina Sees Notable Decline in Country Risk - https://www.riotimesonline.com/argentina-sees-notable-decline-in-country-risk/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9819538145948981
Argentina Slashes Interest Rates in Fight Against Soaring Inflation - https://www.riotimesonline.com/argentina-slashes-interest-rates-in-fight-against-soaring-inflation/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9845226781512715
Bolivia’s Economic Strategy Amid Dollar Drought - https://www.riotimesonline.com/bolivias-economic-strategy-amid-dollar-drought/ - Anthony Albanese unveils millions for critical minerals projects to fend off Chinese supply chokehold - https://www.news.com.au/national/politics/anthony-albanese-unveils-millions-for-critical-minerals-projects-to-fend-off-chinese-supply-chokehold/news-story/4c5a2336f9f55aac26bc8361c94dd07a?from=rss-basic - 0.9829541642595394
Colombia Faces Stubbornly High Inflation Despite Efforts - https://www.riotimesonline.com/colombia-faces-stubbornly-high-inflation-despite-efforts/ - Jobs market outperforms expectations in March as rate cut hopes falter - https://www.news.com.au/finance/work/at-work/australian-economy-sheds-6600-jobs-as-unemployment-rate-edges-higher/news-story/616444dc4d974197cfd6166b07c49822?from=rss-basic - 0.9815987486375105
Caribbean Crisis: Oil Spill Drifts from Tobago to Bonaire - https://www.riotimesonline.com/caribbean-crisis-oil-spill-drifts-from-tobago-to-bonaire/ - Reason passenger plane purposely sunk - https://www.news.com.au/travel/travel-updates/travel-stories/reason-passenger-plane-purposely-sunk/news-story/1aa225ca1f2b02b8fd214361dc26fc38?from=rss-basic - 0.9811032974641699
"""


def main():
    queue = multiprocessing.Queue()
    pa = Process(target=extract_articles, args=(BASE_DIR, NEWSPAPER_A, DAY, START_TIME, END_TIME, queue, "A"))
    pb = Process(target=extract_articles, args=(BASE_DIR, NEWSPAPER_B, DAY, START_TIME, END_TIME, queue, "B"))
    pa.start()
    pb.start()
    articles_a = None
    articles_b = None
    (label, articles) = queue.get()
    if label == "A":
        articles_a = articles
    elif label == "B":
        articles_b = articles

    (label, articles) = queue.get()
    if articles_b is None:
        articles_b = articles
    else:
        articles_a = articles

    del label
    del articles

    new_a = []
    new_b = []

    for article in articles_a:
        article = calculate_nlp(article)
        new_a.append(article)

    del articles_a

    for article in articles_b:
        article = calculate_nlp(article)
        new_b.append(article)

    del articles_b


    simils = []
    for article_a in new_a:
        for article_b in new_b:
            (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"], COSINE_THRESHOLD)
            if similarity:
                simils.append((article_a, article_b, percentage))

    for simil_triple in simils:
        at = simil_triple[0]["title"]
        an = simil_triple[0]["news_url"]
        bt = simil_triple[1]["title"]
        bn = simil_triple[1]["news_url"]
        print(f"{at} - {an} - {bt} - {bn} - {simil_triple[2]}")


if __name__ == '__main__':
    main()
