import os
import cohere 
from dotenv import load_dotenv
import logging

load_dotenv()

co = cohere.Client(os.environ.get('COHERE_API_KEY'))

def cohere_summarize(content):

    response = co.summarize( 
      text=content,
      length='medium',
      format='bullets',
      model='command-nightly',
      additional_command='',
      temperature=0.3,
    ) 
    return response.summary

def generate_revised_title(article_title, article_content):
    revised_title_prompt = (
        f"Title:\n{article_title}\nContent:\n{article_content}\n---\nYour task is to give a revised title for the above article, do not include any clickbait words and represent the actual content of the article\n---\n"
    )
    logging.error("Error: Title generation failed, Switching to Fallback Model")
    return cohere_summarize(revised_title_prompt)

article_title = 'Mobile OS maker Jolla is back and building an AI device'

article_content = "\nOn the fringes of MWC, the worldÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s biggest mobile phone show, TechCrunch is getting a demo of a new kind of AI device. The small black box sitting in front of us on a table in a hotel lobby in Barcelona is designed to tap into the generative AI boom ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” making it another example of how the wheel of innovation is spinning up again in mobile.\nIts maker ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” Jolla, a born-again startup with the combined forces of around 40 seasoned staff behind this new push ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” is building whatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s being tentatively described at this early product design stage as a private and secure ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœblackbox for your lifeÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â.\nThe device is intended as a private-cloud-cum-AI-router that makes the userÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s data accessible for running AI queries. So this device-in-the-making is akin to the personal server concept thatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s been kicking around in privacy circles for years ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” but reconfigured for the generative AI age.\nHere at MWC 2024 weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re hearing a lot of chatter about ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœnext-generationÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â smart assistants, with telco talk rife with predictions that the end of apps as weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™ve known and tapped on them is nigh as generative AI models rewrite the user interface rules. Jolla is jockeying to insert itself into this buzzy conversation by putting the focus squarely on privacy and security ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” since the assistive data processing will take place on the AI device itself.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœWe donÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t believe itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s a good model to put AI run locally here in the phone. ItÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s not secure,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â argues co-founder Antti Saarnio. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœYou can never make smartphones secure enough for that. We believe that in this AI era privacy becomes much more important.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nThe machine learning databases Jolla is architecting to host the userÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s personal information inside the AI device are being designed to intelligently respond to natural language querying and/or proactively surface insights ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” drawing on trusted access to the userÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s mobile data and digital services.\nJolla is building on open source AI large language models, including MetaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s LLaMA 2, for the foundational layer of generative AI smarts. Saarnio says the role for the team is basically architecting the user interface and function design ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” rather than needing lots of AI engineers itself, as theyÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re able to draw on powerful open source general purpose AIs.\nA private data hub for AI\nDiscussing the vision for the product, Saarnio argues that amped up AI models, such as large language and multimodal models, and the powerful data mining and inferences associated with generative AI, change the game when it comes to processing personal information ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” whether itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s emails, calendar, contact lists or obviously sensitive stuff like health data ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” bringing both the potential for AI-powered insights to create huge value and utility for individuals; but also deep risk if the user has to offer up intimate access to their information in order to tap into these services.\nThis trade-off is the problem Jolla wants to fix by designing a way for users to gain the superpower of advanced AI without having to let data-hungry third parties gobble their privacy.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœThis device will hold all your private information,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he says, laying a hand on the small rectangular box weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re discussing. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœIt runs its AI here. All your data will be here and nobody else will have access to it ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” only you.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nAI is increasing data concentration and leading to the development of rich databases of personal information that can be ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœdangerousÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â if exported, he suggests. So what if people could just own their own safe and secure hub where all that processing happens?\nAssuming JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s product is as safe and private as they claim it will be, the level of data protection a user might gain would depend on how much AI processing theyÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re willing (or able) to route via the device. But if they practice good privacy hygiene generally such a product could help people limit their privacy risk when using generative AI.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœIf people use different email clients, and so on, we need to connect to those applications via our API,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â Saarnio notes. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœBut the key hereÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â¦ is weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re saying that your concentrated data is in safe place.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœSurprisingly, we havenÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t seen anyone who is really focusing on data privacy and keeping the data secure,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he adds. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœI think itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s a good play place for us to play.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nThe Finnish mobile phone startup tried very hard to disrupt the traditional mobile smartphone business a decade+ ago, with their alternative, Linux-based Sailfish OS platform. ItÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s that same familiar brand name stamped in tiny letters on the 3D-printed prototype. But the product represents a leap in a new direction for the mobile also-ran.\nSaarnio, an original Jolla co-founder, has returned to what his LinkedIn account simply refers to as ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœNew JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” reenergised and raring to go after winning a long legal battle to reclaim the business and its assets from majority Russian owner, Rostelecom. The mission: Rebuild Jolla anew by building new AI products. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœI think we can completely rebuild this. But we need to do new things,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he tells TechCrunch.\nThe Jolla brand name still has value, as Saarnio tells it. He talks in terms of co-designing the product with the community of Sailfish users and Jolla enthusiasts still excited about what alternative tech can do. But ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” to be crystal clear ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” the AI device wonÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t need special mobile hardware to function. The goal is for this to piggyback on top of mainstream mobile platforms.\nAdding a layer of security and privacy to platforms and apps is exactly the point. The broad ambition, if Jolla can pull in the users and build momentum, is to develop the product into a platform of its own ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” further extending the embedded AI assistantÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s utility by attracting other developers to build apps that operate through its protective wrapper of privacy and security.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœThatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s our only playfield,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â admits Saarnio of the focus on privacy and security. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœObviously, big companies will do similar thingsÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â¦ [But] we can become an open application platform as well for others who are focusing on [AI innovation] so we donÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t need to do the lifting only ourselves.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nHe also predicts big changes incoming for mobile apps over the next few years, driven by AI. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœIt will become almost like a protocol level,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he suggests, describing a scenario where mobile apps are pushed into the background as generative AI interfaces take over. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœYou [wonÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t] really go and open apps anymore. So this whole visible UI level is layer is disappearing.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â \nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœI donÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t know what it means. Basically, nobody probably yet knows, but itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s a major change,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he adds, arguing Jolla is well positioned to take advantage of the shift give its expertise in operating system development. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœAn operating system player like us, we have a good role there. Because our job is to integrate with different applications. Even the app runtime that we have is quite good for that. It gives us access to integrate into different applications, their APIs and so on.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nJolla MindÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â²\nThe prototype sitting on the table currently bears the name Jolla MindÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â² ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” a play on the idea of AI providing humans with a ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â˜second brainÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™. Jolla also described the system as an ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœadaptive digital assistantÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â.\nThe main target customer looks likely to be Android smartphone users as it could offer them a way to tap into the utility of advanced AI without having to expose all their personal data to Google (or other non-trusted third parties) ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” with all the associated risks. (Google remains an attention-mining advertising company, after all. While Microsoft, a major investor in OpenAI, has its own digital advertising business. And Facebook-owner and LLaMA developer MetaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s business model is still pure surveillance advertising.)\nOn the flip side, Apple already offers its own privacy promises and on-device AI processing. It also has its own generative AI products in the works. So value certainly looks harder to build on iOS (where this kind of functionality is likely to be natively embedded). But what Apple will do is not giving Jolla pause. Android remains the dominant mobile platform, with billions of users worldwide, so thereÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s more than enough of a potential addressable market to target ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” especially if advances in AI trigger a rise in privacy concern.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœVery large companies nowadays are very tempted to use our information for AI training ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” because thatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s the name of the game at the moment. So I wouldnÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t trust any company [not to use my data for AI] training,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â says Saarnio. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœIf the future would be similar to the past ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” only a couple of massively big companies were able to take the whole market with AI ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” then I think itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s not very good news for us human beings.\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœIn this past mobile era, we were the data product, basically. But if we let AI steer us we become digital robots, basically ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” the manipulative capability of AI is so big that we donÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t have a chance. So thatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s why I think we need digital clarity. And thatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s our role.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â\nÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœBasically, you need AI. But you need to be mastering the AI so that the AI is not mastering us,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he adds.\nImage Credits: Natasha Lomas/TechCrunch\nSaarnio himself built the first product mock ups, after spending the last 1.5 years learning to program ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” upskilling from his former finance-focused background to close in on the AI opportunity.\nHe describes MetaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s decision to open source LLaMA as the ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœbreak pointÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â for this new wave of AI innovation. And is ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” necessarily ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” hopeful there wonÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t just be a repeat of the last mobile cycle where Big Tech took most of the spoils. ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœI think it will be difficult for big players to own this agenda,ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â he predicts of generative AI.ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â \nDuring a brief demo of the JollaMindÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â² prototype ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” the first time it was shown to press, weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re told ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” we saw JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s AI assistant software running on a mobile phone which was interfacing with AI systems and databases running on the prototype hardware. The developer running the demo posed a couple of natural language questions and received contextually relevant responses back, voiced by a rather deep-throated robot voice, which added to the spooky thrills (so JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s app is doing speech generation too).\nIn one of the demo examples, the developer asked the software ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœwho is Natasha?ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â. JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s AI assistant responded by parroting my TechCrunch biog ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” without needing to be provided with additional context since the AI has access to calendar info, emails etc where it could infer the subject of the enquiry from just a first name.\nIn another demonstration, the developer asked the AI ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœwhat tasks do I have for Tuesday?ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” and got a read out of their calendar items with observations about the priority of different items.\nBoth examples are fairly utilitarian, in terms of what AI assistance features can do, but the point is the user of JollaMindÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â² can rest assured their information remains safe from prying third parties.\nAnother envisaged use-case Saarnio sketches is email triage: Where the AI assistant could keep tabs on incoming emails and surface priority messages, including knowing whether to override a ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â˜do not disturbÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™ setting to make sure something important isnÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t missed.\nWhile such AI-powered email parsing functions do already exist (and can even be baked in by email providers themselves, as Google does with Gmail ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â˜smartÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™ features), you have to be comfortable providing a cloud-based entity with access to your inbox to tap into such smarts ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” which is a privacy and security trade-off.\nJolla also sees potential for business users ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” such as a smart minutes type feature. Saarnio gave the example of lawyers meeting with clients who could ask them if they could record the meeting to make it ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœmemorableÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” meaning it would be captured by the device and a searchable record of when (and what) was said retained to aid productivity but with all the sensitive data remaining on the private cloud device.\nIn instances where a user might actively want to go outside JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s system in order to make use of a specific third party AI, the product could pop up a permissions screen for them to approve sharing their data ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” so the user could manually accept extra risk on a case-by-case basis. The device could also let users configure which kind of questions they only want processing locally (health queries, say) and which ones theyÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re happy for the device to cast a wider net out to third party AIs.\nThe sneak peak weÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™re getting is just that: A glimpse of whatÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s coming down the pipe. The final form-factor, features and specs ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” even, for example, such as whether it might have a screen, built-in speaker, its own battery or keyboard, or stay as a minimal black rectangle ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” remain tbc. So much of the product design and detail ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” and even core utility features ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” is yet to be nailed down. But Saarnio does say the device will be priced below ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â¬300.\nHe also points out the hardware can act as an upgrade for a userÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s existing mobile phone, saying it can bring advanced AI processing capabilities to even mid-tier mobiles. So an old smartphone you have lying around in a drawer could get a second lease of life with JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s AI layer bolted on top.\nWhatever form the device finally takes, Jolla is envisaging it as something generally static ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” rather than a second mobile device you have to carry with you. So the likely scenario is it gets stored safety by the user at their home or office. But itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s available to be queried remotely through the userÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s own mobile device (with, likely, a layer of biometric security looped in to ensure the dynamic database of their life it contains remains safe).\nBack to the future\nSo what happened to old Jolla? Wind back the clock to August 2021 and the company as it then was had just turned profitable after a decade of hard slog selling its alternative OS and app support platform. Then, in spring 2022, disaster struck as Russia invaded Ukraine, putting JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s non-Russian shareholders in a bind and desperate to cut ties with Russia.\nSaarnio says company shareholders they tried for a long time to negotiate with Rostelecom directly to buy back its majority share. However the Russian telco would not budge. So, in the end, they changed tack to litigation ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” and a court adjudicated corporate restructuring process in Finland enabled them to buy back the old assets. The court decision on that restructuring came around October last year ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” handing the team a clean slate to take a fresh swing at mobile innovation, now with AI front and center.\nThe new incarnation of Jolla will be fully focused on AI devices. But the legacy story doesnÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™t end entirely. Separate ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Âœindependently fundableÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â business entities are being established ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â” one to look after JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s tech focused on in-car systems and app support for car makers, and another for Sailfish mobile devices for businesses, per Saarnio. But he and his team will be fully focused on rebuilding Jolla as a new, and they hope smarter and more agile, AI startup.\nMark your calendar: May 20 will be the official announcement of JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s first AI product. The date has been picked as itÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s a decade on from the ÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚ÂœJolla Love DayÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â announcement of May 20, 2013, when the Sailfish maker revealed its first ever mobile phone. Which is a neat way to underscore the cyclical nature of technology.\nIn just under three monthsÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™ time the exact shape, specs and feature set of the AI device will be clearly defined and a pre-ordering campaign will likely kick off at that point too. As for shipping, Saarnio is confident they can get the JollaMindÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â‚ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â² to market later this year. Expect JollaÃƒÂƒÃ‚ÂƒÃƒÂ‚Ã‚Â¢ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â€ÃƒÂƒÃ‚Â‚ÃƒÂ‚Ã‚Â™s new baby to arrive in Q4.\n\n"

print(generate_revised_title(article_title,article_content))