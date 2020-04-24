# Mapping the Personal Identity in the *Treatise* through Expert Knowledge

## 1. Introduction to the Project

Hume published his *Treatise of Human Nature* in 1739. It’s an enormous text that covers an incredible range of philosophical topics. The text is divided into 3 books, each of which is divided into 3-4 parts, each of which contains 7-17 chapters of varying lengths [for our purposes, each paragraph in those chapters is also numbered]. The Treatise also has philosophically interesting material in its Appendix and Abstract which were written and added to the Treatise more than a year after its initial publication.

The copy of the *Treatise* that I'm working with can be found in a TXT form [in this repository](./Full Treatise in HTML.txt). It was acquired from [davidhume.org](https://www.davidhume.org)

My aim in this project is to develop a tool that maps Hume’s Treatise by philosophical topic. To construct each map of a given topic, I want to use the scholarly literature produced in the last century or so which discusses Hume’s views on that topic. In order to use the scholarly literature, my plan is to look at the articles in that literature to see which parts of Hume’s texts are cited.

The project’s guiding thought is that the more frequently a portion of the Treatise is cited by scholars working on Hume, the more relevant and important it is to understanding Hume’s views on the topic. Such information is not only a useful tool for novices to Hume’s philosophy. It’s also useful for expert scholars working on a topic as it can be used in reverse to see which publications make novel use of portions of Hume’s Treatise that aren’t usually brought into discussions of a given topic. More on other potential uses of the project later.

To start this project off, we’re going to look at the scholarly literature that examines Hume’s views on personal identity. To collect the set of scholarly works on Hume’s views of personal identity, we can consult the index, [philpapers.org](https://www.philpapers.org), an indexing website managed by area experts. Philpapers has a section dedicated to works on Hume, which is subdivided by topic. The personal identity leaf is available here: [David Hume - Personal Identity](https://www.philpapers.org/browse/hume-personal-identity)

## 2. Project Goals

I envision several uses for the proejct.

### a. Uses for Novices

Newcomers to Hume's philosophy may be interested in his theory of personal identity for any number of reasons. Perhaps they are graduate students taking a class on Early Modern Philosophy that only briefly touched on some parts of Hume's philosophy but not as much as the student would've liked on his theory of personal identity. Perhaps they are a philosopher who works in contemporary philosophy of mind or self and would like to quickly find some of the most useful parts of Hume's texts to engage with and think through. Perhaps they have done work on buddhist conceptions of self and have heard that Hume bears interesting similarities to Buddhist conceptions of self and would like to read more, etc. There may be any number of reasons that someone who is not a Hume scholar becomes interested in learning more about Hume's theory of personal identity.

Reading a massive book like the *Treatise* is not likely to be a project that any of these people would undertake. Moreover, in a deeply systematic work like the *Treatise* a table of contents isn't as useful as one would hope. Relevant pieces to Hume's theory of personal identity are likely to be spread in various places around the *Treatise*, including unexpected places that don't superficially look like they should have anything to do with personal identity. Hume scholars, of course, have exhaustively studied the *Treatise*. The results of their research is published in journals, books, and other scholarly literature. By extracting where scholars are quoting from the *Treatise*, we can capture much of their expert knoweldge for the use of novices. The upshot, then, is a reading list, ordered by importance, composed of chapters in the *Treatise* that novices could focus on to get quick access to the relevant parts of the *Treatise*.

### b. Uses for Experts

Once we have the entire body of scholarly literature mapped, we can use that set as a whole to provide some tools for Hume Scholars. For example, it would be nice to compare a particular article, or all of the articles by a particular scholar, or a particular set of articles, etc., to the body of scholarly literature as a whole. This would be useful to establish that certain scholars or certain families of views put greater emphasis on certain parts of the *Treatise* rather than others that are more common in the scholarly literature as a whole.

For another use, if I, as a Hume Scholar, was struck by something I read in a certain part of the *Treatise*, I might want to look up any see which, if any, articles have discussed that part of the *Treatise*.

For another use, I might want to make a claim in a research publication about the frequency of discussion or emphasis scholars place on a certain part of the text.

For another use, in my research I might have placed particular emphasis on some passages from the *Treatise*. To ensure that I'm doing a good job engaging all of the existing literature, I could use the database to see what other articles discuss those paragraphs frequently.

For another use, I might want to evaluate the impact of a certain article. For example, if we look at how citations to the *Treatise* have changed over time, we might find that some parts become discussed more frequently or less frequently. We could then try to identify the articles that first made heavy use to determine the impact of those articles in generating more discussion about those passages. Impact is notoriously tricky to evaluate in the humanities and philosophy in particular as philosophers have notoriously terrible practices of citing each others' work. This could provide experts a way to measure their own or others' long term impact.

And so on. The theme in all of these expert uses of the information here is that we need a tool that allows us to compare the literature as a whole to different slices of it (or slices of it to itself).

### c. Input into a Larger Mapping of the *Treatise*

The philpapers indexing site has over 13,000 publications, divided into over 80 categories. Over time I hope to map *all* of these categories. With all of the categories mapped, we would then have a full conceptual map of the *Treatise* based on the expert knowledge of Hume scholars. At that point there are lots of interesting questions to ask about Hume's philosophy more broadly. For example, perhaps he has interesting overlapping discussions of concepts that aren't often linked. Etc.

Similar projects could be conducted over various philosophers from the early modern period and then inter-philosopher comparisons could be conducted.

These projects are very far down the line.


## 3. Project Phases

### a. Phase One: Constructing the dataset

Assigning each paragraph in the Treatise a score that represents the frequency it is cited by scholars requires counting citations to each paragraph in the Treatise. To perform such counting, we need to take the following steps.

+ First, we have to determine all of the relevant publications, gather them, and prepare them for search.

+ Second, we need to search each paper for citations to the Treatise.

+ Third, we need to credit each paragraph each time it is mentioned in a citation.

*As of April 24, 2020, the main tasks here have been completed. There is some fine tuning, but the tools are largely in place to generate a dataset. The refining that needs to be done here largely concerns refining some of the search phrases to extract citations out of articles.*

*For more detail on these processes, see [Citation Extraction Process](./Citation-Extraction-Process.md)*

### b. Phase Two: Making use of the dataset

Once we have a data set, we need to develop some tools or analyses to underlie a product that is usable in the ways describe above in Section 2. One tool it looks like we'll be using is Tableau for generating visualizations of the citation patterns in the literature across the *Treatise*.

Other tools could be text based tools. For example, a tool for generating and ordering a reading list based on the scores of the paragraphs in each chapter. Another could be a reverse look up tool that takes as input a chapter or paragraph from a user and returns a list of publications, ordered by how much they contributed to the paragraph or chapter's total score.

Finally, another tool might create clusters of papers based on the similarities in their citations. That tool would allow you to enter a paper or publication and find what other papers are most similar to it in terms of the *Treatise* passages they discuss.

*As of April 24, 2020, only the most basic elements of Tableau work have started. Everything else is tbd. You can find it [here](https://public.tableau.com/profile/matt.priselac#!/vizhome/PersonalIdentityintheTreatise-Overview/Sheet12?publish=yes)*

### c. Creating a product

Once we have the data and the tools, I aim to create a usable product that anyone could access and use at will for the purposes described  above. Here we'd need some user interface design, probably a website to host the interface and data, etc.

*No work has been done on this front*
