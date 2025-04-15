# seed_articles.py

from app import create_app, db
from app.models.models import Article, Source
import datetime

app = create_app()

with app.app_context():
    # 确保至少有一个 Source
    source = Source.query.first()
    if not source:
        source = Source(
            name="BBC",
            url="https://www.bbc.com",
            description="BBC News - Trusted world and UK news source",
            logo_url="/static/images/Screenshot 2025-04-15 at 13.47.48.png"
        )
        db.session.add(source)
        db.session.commit()

    # 你要插入的文章数据
    articles_data = [
        {
            "title": "第一篇测试文章",
            "content": """CNN
 — 
Only three months into his new term, President Donald Trump is escalating a battle against institutions that challenge his strongman instincts, including the courts, the legal profession, elite education and the media.

The administration is projecting presidential authority in a broader and more overt way than any modern White House. Its expansive interpretation of statues and questionable interpretations of judges’ rulings is causing alarm about its impact on the rule of law, freedom of expression and the Constitution.

“There’s something broken,” Trump said in the Oval Office on Monday. “The liberal establishment – but they’re not running things anymore in this country.”

He sat beside President Nayib Bukele of El Salvador, who brands himself as the world’s “coolest dictator” and whose huge popularity is based on a brand of elected authoritarianism Trump admires. The warmth lavished on a leader who’d have been treated as a pariah by a conventional US administration was a ominous window into the 47th president’s future intentions.

Bukele has suspended parts of the Salvadoran constitution and imprisoned tens of thousands of people without due process in a crackdown against crime.

He suggested Trump might try something similar. “Mr. President, you have 350 million people to liberate, you know. But to liberate 350 million people, you have to imprison some. You know, that’s the way it works, right?”

Trump’s own hardline aspirations were revealed in the meeting through the prism of his increasingly ruthless deportation policy, which is raising profound questions about apparent abuses of due process and human rights.

Both presidents relished the chance to publicly refuse to release an undocumented migrant who was seized in Maryland and deported to a notorious mega-prison in his native El Salvador without a court hearing and despite a judge’s order that he should not be sent back to the country.

The White House is refusing to act on another judge’s order that Kilmar Armando Abrego Garcia should be brought back to the US and is walking a fine line on a Supreme Court decision saying it must facilitate his return. It says Abrego Garcia is a gang member and terrorist despite producing no public evidence. It also argues that US courts have no jurisdiction because Abrego Garcia’s fate is bound up in Trump’s power to set foreign policy.

The Supreme Court ruled 9-0 last week that the administration must “facilitate” the return of Abrego Garcia after it admitted expelling him over an administrative error. But the White House is using its rather imprecise language – perhaps motivated by a push for unity or a desire to avoid a direct constitutional showdown – to claim the justices endorsed its position, rather than rebuking it.

“I think the Supreme Court is responsible to some extent because they diced words,” retired judge Shira Scheindlin told CNN’s John Berman on Monday. But Scheindlin warned the administration was entering dangerous ground. “What we have here is a defiance of the Supreme Court order. The Supreme Court said facilitate his return and expedite it.”

Scheindlin added: “It’s defiance which puts us on the edge of a constitutional crisis between the judicial branch and the executive branch.”

Laurence Tribe, a renowned constitutional scholar, told CNN Monday that the administration’s defiance made it likely the case would end up back before the Supreme Court – which would then face a fateful choice. “It is not just immigrants who are subject to this kind of game. It is a deadly game that could be played with any citizen,” Tribe, professor emeritus at Harvard Law told Kaitlan Collins, who had earlier questioned Trump and Bukele in the Oval Office. “The president has already begun to play it. That is not the country that any of us I think grew up in.”

Indeed, Trump is mulling an even more flagrant challenge to the law. He suggested that his scheme to deport those who he says are gang members and terrorists to harsh El Salvadorian prisons could be widened.

“I’d like to go a step further, I mean … I don’t know what the laws are. We always have to obey the laws,” Trump said, looking at Attorney General Pam Bondi on a White House sofa. “But we also have home-grown criminals that push people into subways, that hit elderly ladies on the back of the head with a baseball bat when they’re not looking, that are absolute monsters. I’d like to include them in the group of people – to get them out of the country.”

The idea that the administration would ignore constitutional protections available to all Americans, even those who are incarcerated, and deport them to draconian prison camps overseas might strain credulity. But Trump’s words came amid an atmosphere of growing authoritarianism around his White House and an apparent determination to reject constitutional constraints on his behavior.""",
            "image_url": "/static/images/Screenshot 2025-04-15 at 11.40.29.png"
        },
        {
            "title": "China urges Vietnam to resist ‘unilateral bullying’ as Xi tries to rally region in face of Trump tariffs",
            "content": """Hong Kong
CNN
 — 
Xi Jinping has urged Vietnam to resist “unilateral bullying” and uphold free and open trade, as he begins a high-stakes diplomatic tour of the region’s major export-reliant economies in a bid to position his country as a stable partner in contrast to the United States.

The Chinese leader arrived in communist-ruled Vietnam on Monday and is set to visit Malaysia and Cambodia from Tuesday to Friday — countries that have seen growing trade and investment ties with China in recent years.

In meetings with Vietnam’s top leadership Monday, Xi said the two countries should work together to maintain “the stability of the global free trade system and industrial and supply chains,” according to Chinese state news agency, Xinhua.

“China’s mega market is always open to Vietnam,” Xi was quoted as saying by Xinhua, adding that “China and Vietnam should strengthen strategic focus and jointly oppose unilateral bullying.”

“A small boat with a single sail cannot withstand the stormy waves, and only by working together can we sail steadily and far,” he said.

The in-person trip comes just days after US President Donald Trump paused his “reciprocal” tariffs on most countries for 90 days — narrowing the focus on his trade war squarely on China.

As Washington and Beijing exchange record-high levies, Southeast Asian nations, still catching their breath from the now-suspended US tariffs, are growing increasingly anxious about being caught in the crossfire between the world’s two largest economies.""",
            "image_url": "/static/images/Screenshot 2025-04-15 at 11.41.37.png"
        },
        {
            "title": "Hamas rejects Israeli ceasefire disarmament proposal, Palestinian official says",
            "content": """Hamas is said to have rejected an Israeli proposal for a six-week ceasefire in Gaza which called for the armed group to give up its weapons.
A senior Palestinian official familiar with the talks said the plan gave no commitment to end the war or for an Israeli troop pull-out - key Hamas demands - in exchange for releasing half of the living hostages which it holds.
It comes as Israel continues its military offensive in Gaza.
A security guard was killed and nine other people were injured in an air strike on a field hospital in Khan Younis, the hospital said. The Israel Defense Forces (IDF) did not immediately comment.
A UN agency meanwhile warned that "the humanitarian situation in Gaza is now likely the worst it has been in the 18 months since the outbreak of hostilities".
It is six weeks since Israel allowed any supplies to enter through crossings into the Palestinian territory - by far the longest such stoppage to date.
UN agencies strongly refute Israel's claim that there is enough food in Gaza to last for a long time and suggest the blockade could breach international humanitarian law.
Israel's prime minister said the block on supplies was aimed at pressuring Hamas to release hostages and to extend the ceasefire which expired on 1 March.
At the same time, the UN's humanitarian affairs office stated: "Partners on the ground report a surge in attacks causing mass civilian casualties and the destruction of some of the remaining infrastructure that's needed to keep people alive."
""",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.23.49.png"
        },
        {
            "title": "Trump blames Zelensky for starting war after massive Russian attack",
            "content": """Trump on Monday had first described the attack as "terrible" but said he had been told Russia had "made a mistake". He did not give further detail.
Moscow said it had targeted a meeting of Ukrainian soldiers, killing 60 of them, but did not provide any evidence.
Meanwhile, Ukrainian media reported that there had been a medal ceremony for military veterans in the city on the day of the attack. Zelensky sacked Sumy's regional chief on Tuesday, for allegedly hosting the event, local media reported.
Trump on Monday also blamed his predecessor Joe Biden for the war's casualties- which are estimated in the hundreds of thousands, not the millions he's claimed.
"Millions of people dead because of three people," Trump had said. "Let's say Putin number one, let's say Biden who had no idea what the hell he was doing, number two, and Zelensky."
Questioning Zelensky's competence, he said the Ukrainian leader was "always looking to purchase missiles".
"When you start a war, you got to know you can win," the US president said.
Trump has repeatedly blamed Zelensky and Biden for the war, despite Russia invading Ukraine first in 2014, five years before Zelensky won the presidency, and then launching a full-scale invasion in 2022.
Trump further argued on Monday that "Biden could have stopped it and Zelensky could have stopped it, and Putin should have never started it. Everybody is to blame".
Tensions between Trump and Zelensky have been high since a heated confrontation at the White House in February, where the US leader chided Ukraine's president for not starting peace talks with Russia earlier.""",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "3",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "4",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "5",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "6",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "7",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
        {
            "title": "8",
            "content": "更多的内容。",
            "image_url": "/static/images/Screenshot 2025-04-15 at 21.25.33.png"
        },
    ]


    # 插入所有文章
    for data in articles_data:
        article = Article(
            title=data["title"],
            content=data["content"],
            image_url=data["image_url"],
            published_at=datetime.datetime.utcnow(),
            source_id=source.id
        )
        db.session.add(article)

    db.session.commit()
    print(f"插入了 {len(articles_data)} 篇文章 ✅")
