
**Dab, Deborah**
0:03
I'm just gonna assume like it's a Tier 3, I don't know. And then it would. It would not have all of the tiers listed. It would just say this is a Tier 3 drug, so your benefits would be as follows.

**Nguyen (Tran), Nhi**
0:17
So like I think this is a good example in that different benefits may use the same formulary, right? Like some groups have the same formulary and their benefit says you have no weight loss coverage. Another group uses the same formulary and has a different benefit.
**Nguyen (Tran), Nhi** 
0:37
That says you do have weight loss coverage. Another group may actually have a third flavor, like use the same formulary and only have weight loss coverage under limited situations, right? Which you wouldn't get in like a formulary file because the formulary file will still say WAGOBI is on that.

**Dab, Deborah**
0:37
Mhm.

**Nguyen (Tran), Nhi**
0:55
But I'm not sure how the EOC actually explains that too, so that you get like the accurate cross section between benefits and formulary.

**Dab, Deborah**
1:06
I think that's already it would be specified in the EOC and we can ask for some examples of EOC, but the first thing is gonna is going to pull the benefit layer and then it'll check for a formulary associated with that.

**Nguyen (Tran), Nhi**
1:18
Mhm.

**Dab, Deborah**
1:24
So I think it's kind of programmatically how we design it, Gabby, that it's not formulary for, well, the two days has had to converge, but the coverage in your EOC is what tells you how to make use of what's in the formulary.

**Nguyen (Tran), Nhi**
1:43
OK.

**Dab, Deborah**
1:45
We looked. There are fields. Also talk to Vanessa Grover too. There are fields that say which pharmacy details today. Like I said, this is being done today manually through a human.
**Dab, Deborah**
2:04
Basically going in, looking at prescription drug benefits and quoting back these dollar amounts. And then if they don't know that's here, then they're going to reference the formulary manually.
**Dab, Deborah** 
2:20
Um.
**Dab, Deborah** 
2:23
So we're just trying to create a more instantaneous response that's gonna be more accurate than the manual nature of coming through multiple data sources.

**Nguyen (Tran), Nhi**
2:37
OK.

**Dab, Deborah**
2:39
And like I said, there's not really an ask for you. I mean, we we did talk to a few folks on your team to understand, OK, well, we know this data is output into PDFs, but where is it coming from and how often is it changing? And it sounds like RX flex is the source of truth and there's already some data that's being passed to experience cubes, so potentially.
**Dab, Deborah** 
2:58
It's the technical folks like getting on the call where we need to figure out are we reaching into Rxflex? Are we just grabbing that file and loading it on regular cadence into the model? But I wanted to make sure you knew about this since we were going to be poking around.

**Nguyen (Tran), Nhi**
3:14
Yeah, I would say like you, we don't typically direct connect into RX Flex because it's a third party vendor. It's a web-based tool, but for all of our internal reporting purposes, we do a lot of extracts.
**Nguyen (Tran), Nhi** 
3:33
From Rxflex and I think Elaine told you it, the data is an experience cube. You know there are even if that's where we handle this, you know build out our source of truth, the data lives in other systems that are in house versus.
**Nguyen (Tran), Nhi** 
3:52
Connecting to Arts Flex because we can always end up moving away from Arts Flex. So my recommendation would be.
**Nguyen (Tran), Nhi** 
3:59
Like an internal data source instead. Because if you build something into Rxflex and we decide we're not going to use Rxflex anymore one day, then that could be problematic.

**Dab, Deborah**
4:02
Mhm.
**Dab, Deborah** 
4:13
What do you Where do you consider the source of truth for the formulary data?

**Nguyen (Tran), Nhi**
4:19
Well, we we house it in Rxflex with our intent, right? Because it has the interface for us to update it on a regular basis in the formats we need to. But when the we the data is exported and goes back into experience cube. So if we want to look at what is.

**Dab, Deborah**
4:37
OK.

**Nguyen (Tran), Nhi**
4:39
The data or intent as of a certain date, then we should use experience cube, because if we change vendors, we'll have to also update the source to experience cube, right? So you're really looking at the connecting to the data rather than.
**Nguyen (Tran), Nhi** 
4:54
The application, yeah. Mm-hmm.

**Dab, Deborah**
4:55
It's just that. Mm-hmm.
**Dab, Deborah** 
4:59
OK.

**Nguyen (Tran), Nhi**
5:00
I don't know if, Andy, Elaine, you guys think different, but that's what I would recommend that we connect into the source of truth in our own data.

**Dab, Deborah**
5:01
It.

**Trinh, Andy**
5:11
Yeah, it it don't we have like the data stored in Book of Records 'cause I know like right now like the Jason files get sent to Book of Records.
**Trinh, Andy** 
5:27
Is there a way to where we don't have to if we change vendors, whether we can just use the data resources from what's provided to book of records?

**Dab, Deborah** 
5:41
I I'm not going to speak architecturally, but I think that that is sound right. Wherever you are already putting the data for it to float through to where you are using it, we should connect it.

**Trinh, Andy** 
5:54
Yeah, 'cause then that will solve for any. If we in a future state, if we don't stay with Rxflex, it the future vendor will still have to supply book of records and then the data can be pulled. That experience cube aspect can be pulled from there.

**Dab, Deborah** 
6:17
And.
**Dab, Deborah** 
6:26
Right now, like I said, this is Q2 scheduled, so that means likely end of Q2 when anything would be live, but we'll make sure. I'm sure in the background that this large folks will be partnering to understand that data source and to connect it. We'll feed it through some tests.
**Dab, Deborah** 
6:43
But we will list you as stakeholders and before we go live, make sure that you're aware of what this looks like in the next iteration.

**Nguyen (Tran), Nhi** 
6:51
And who who tests? Who will test out like the accuracy of the data? I mean, I don't know how AI is built, but of my concerns with like, yeah.

**Dab, Deborah**
7:00
The accuracy, yeah, um.
**Dab, Deborah** 
7:08
The validation of the output is being done by our customer service team. They have the Quality Assurance team that already reviews benefit inquiries against criteria that's required for quality and for the local OPS scorecard.
**Dab, Deborah** 
7:26
Like I said, this is not a new, we're not creating a new type of response. We're just automating the way we get to it. So that team's going to be validating what true is. If you think there's somebody else, we should run the any test data by. We're more than happy to include them for a review.

**Dab, Deborah** 
22:13
I've heard all of that is just like a a barka stuff.

**Nguyen (Tran), Nhi** 
22:17
It in the background, yes, all that mock adjudication that Gemini presents to like the provider or that interface that customer care is using is Gemini, but all the engine behind it is connected into Darwin mock adjudication, yeah.

**Mirsaidi, Gabrielle** 
22:17
OK.
**Mirsaidi, Gabrielle** 
22:33
I want to. I definitely want to explore this further. Who? Who could we chat with? Who would know Darwin and Gemini and Abarka to see what the technical capability is?

**Nguyen (Tran), Nhi** 
22:47
Selena's team. Selena Wong. Mhm.

**Mirsaidi, Gabrielle** 
22:49
Selena. Oh, OK, great. Yeah. Sorry. You know, I've been here, I think, what, six months? And I don't know everybody yet. So I'm working on it. So, yeah, that's what I hear, you know?

**Nguyen (Tran), Nhi** 
22:57
Oh yeah, no worries. Six years and you may still not know. That's OK.

**Mirsaidi, Gabrielle** 
23:05
OK, great. Yeah, this was, this was very helpful. Deb, thanks for organizing this. It's it's definitely intriguing and I want to learn more about what our technical capabilities are to solve this problem for our customer service reps and our members.

**Dab, Deborah** 
23:22
Thanks. And I think between you and Jason, you can share collective knowledge because this is our 4th call. So we have other contexts where we've talked about the other systems a little bit.

**Mirsaidi, Gabrielle** 
23:31
Great. Excellent. OK, cool.