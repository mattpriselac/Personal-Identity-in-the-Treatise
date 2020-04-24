# Citation Extraction Process Explanation

In this document, I'll explain the conceptual process I tried to implement for extracting citations to the *Treatise* from articles.

In broad outline, assigning each paragraph in the *Treatise* a score that represents the frequency it is cited by scholars requires counting citations to each paragraph in the Treatise. To perform such counting, we need to take the following steps.

+ First, we have to determine all of the relevant publications, gather them, and prepare them for search.
+ Second, we need to search each paper for citations to the Treatise.
+ Third, we need to credit each paragraph each time it is mentioned in a citation.

## 1. Gathering the materials and preparing for search

Most materials are easily gathered. They are articles available in PDF format. Publications not available in PDF format need to be requested and scanned into PDF format.

Unfortunately PDF files themselves aren’t very easily manipulated or searched without first extracting the text content out of them. This turns out to be a bit messier than I initially anticipated and the process I settled on to address these difficulties is described in [Processing PDFs](./Processing-PDFs.md). *note: this isn't yet added*

## 2. Extracting the citations to Hume from each paper

Unfortunately, not all citations to Hume’s Treatise have the same format. Citations come in two main flavors.

More recent publications have adopted a standardized format of Book.Part.Chapter.Paragraph. These citations derive from the Norton & Norton edition of Hume’s Treatise, available here. Books, parts and chapters are sometimes specified with arabic numerals, sometimes roman numerals. For example, 1.4.3.25, or I.iv.2. Sometimes these are preceded by ’T’ or ‘Treatise’ or ‘THN’ as in ‘T1.4.3.25’, or ‘Treatise I.iv.2’, or ‘THN 1.3.6.2’.

Citations in this format are relatively straightforward to extract from the text of articles. See Appendix 2 for the regular expressions used to extract these citations. About 1/3 of the articles examined contained citations in this format.
Older research tends to use a version of the treatise edited by Selby-Bigge and Norton (hence forth ‘the SBN edition’). These cite the Treatise by using a page number instead of the structured citation used to cite the Norton & Norton edition. More recently these citations have been prefaced by ‘SBN’, e.g. SBN 320. However, they are often simply page numbers prefaced by a T, THN, or Treatise, e.g. ’T 502’, ‘THN 123’, or ‘Treatise 417’.

Citations prefaced with ‘SBN’, ’T’, ‘THN’, or ‘Treatise’ are easy to extract. About 1/3 of the articles considered contained citations in this format. See Appendix 2 for the regular expressions used to extract these citations.

The most difficult to extract citations, however, are citations to the SBN edition that aren’t prefaced by any of the foregoing. One help, however, is that the page numbers are nearly always enclosed in parentheses and often prefaced by a ‘p’ or ‘p.’ or ‘pp.’. In some cases the page numbers are also prefaced by ‘Hume,’ or ‘Hume’. A second help is that these page numbers only go up to three digits as the SBN edition has only 636 pages. As a first pass at collecting these citations, then, I collected all parts of the text that are inside of parentheses and end with up to a three digit number.

The difficulty with these citations, however, is that merely extracting parentheses that match the described conditions (possibly having some text but ending with up to a three digit number) doesn’t guarantee us that the page numbers we’ve selected are citations to the Treatise. They could, for example, be a citation to the page number of another piece of scholarly work, or to the works of another figure in the history of philosophy. I currently have two further ideas that might help more accurately retrieve only citations from the Treatise.

First, for articles published in the journal Hume Studies, nearly all expressions inside of parentheses that only include page numbers are to Hume’s work. So, when we search articles from Hume Studies, we can somewhat safely just grab all such parentheses enclosed page numbers as citations to the treatise. This means it is important to keep track of the journal from which articles are taken in our data.

Second, as described in Appendix 2, the data structure that I’m using to search and store information about the publications searched and citations discovered therein keeps track of the order of citations. Generally, citation practices are such that you can assume that if a citation only includes a page number in parentheses, e.g. (p. 235) or (235), it is a citation to the same work as was previously cited. And that assumption is safe to carry backwards until you end with a citation that more explicitly describes the work, e.g. (Hume. p. 105), or (Hume, Treatise, p. 105). So, if you track backwards in citations until you find one with a ‘Hume’ or ‘Treatise’ etc. (or some other author) mentioned, you can more safely assume that all citations to only page numbers following that one are (or are not) to the Treatise.

That said, this is the most difficult issue and I’ve not yet settled on any systematic way of settling which citations to page numbers are citations to the Treatise or not.

## 3. Crediting each paragraph when mentioned in a citation

**Note: Some of this gets pretty tedious and in the weeds**

The basic idea here is to start with a list of every paragraph in the Treatise and add a point to each paragraph when it is mentioned in a citation.

So, to start, we need a master list of all the paragraphs in the Treatise. We’ll call this the ‘Master Score Sheet’.

Before we start adding points to paragraph, however, we need to take account for some of messiness in how citations appear in publications. The central complication here is that not every citation mentions only one paragraph. Some mention multiple paragraphs (e.g. 1.4.3.1-3, or 1.4.3.1, 4, or some combination there of. Some citations don’t mention paragraphs at all, but only cite to the level of chapters instead (e.g. 1.4.3 instead of 1.4.3.12).

Depending on the citation, then, there may be up to three stages in the process of crediting a paragraph with a citation mention. I’ll start with the easiest case, which requires only one stage.

*Case 1: Easiest possible case*

Suppose that our citation only mentions one Treatise paragraph. For example:
>1.4.3.12.

In this case, we simply add 1 to the paragraph’s score in the Master Score Sheet.

*Case 2: Paragraph Collections*

Suppose that our citation mentions a collection of paragraphs. For example:
>1.4.3.12, 15

In this case there is only one citation but it contains two different paragraphs. In this case, we will give each paragraph that is mentioned partial credit. There is one citation and it mentioned 2 paragraphs, so we will add 1/2 to each paragraph’s score in the Master Score Sheet. Generally, if there are n paragraphs mentioned in the citation, each paragraph gets 1/n added to its score in the Master Score Sheet.

*Case 3: Paragraph Ranges*

Suppose that our citation mentions a range of paragraphs. For example:
>1.4.3.12-15

In this case there is only one citation but it contains a range of paragraphs. In this case, we need to first enumerate the paragraphs in the range to make a collection and then add points to each paragraph in the Master Score Sheet in the same was as in Case 2. That is, if there are n paragraphs in the range, each paragraph gets 1/n added to its score in the Master Score Sheet.

So, in this example, first we enumerate the range of paragraphs into a collection of
paragraphs:
>1.4.3.12, 1.4.3.13, 1.4.3.14, 1.4.3.15

Second, since there are four paragraphs mentioned in this one citation, each paragraph
gets 1/4 point added to its score in the Master Score Sheet by this citation.

*Case 4: Chapters*

Suppose that our citation mentions only a chapter. For example:
>1.4.3

In this case there is only one citation but it doesn’t contain any paragraphs. It only contains a citation that goes chapter deep into the structure of the Treatise. In this case, we treat it as a range citation and distribute the citation evenly over each paragraph in the chapter. So, if there are n paragraphs in the chapter, each paragraph in the chapter gets 1/n points added to its score in the Master Score Sheet.

So, the first step to assigning credit is to look to the Master Score Sheet to get a list of the paragraphs that are in chapter 1.4.3. Suppose it is 16, ie. the chapter runs from 1.4.3.1-1.4.3.16.

Second, we transform the citation to the chapter into a collection of paragraphs. So, our citation of 1.4.3 becomes:
>1.4.3.1, 1.4.3.2, 1.4.3.3, ... 1.4.3.14, 1.4.3.15, 1.4.3.16

Third, we then add 1/16 points to each paragraph’s score in the Master Score Sheet.

So far, all of the cases we’ve considered are straightforward because they are in the Norton format which specifies a paragraph or chapter. However, that only covers one of the two kinds of citations mentioned above in Stage 2. The other kind of citation, citations to the SBN edition, use page numbers. Converting page numbers into paragraphs adds another layer of complexity to the process of crediting paragraphs in the Master Score Sheet.

#### Converting citations to the SBN edition into paragraph credit

The first layer of complexity comes from the fact that paragraphs do not correspond one to one with page numbers. For example,
+ Paragraph 1.1.1.1 might span two pages in the SBN edition, from page 1-2.
+ Paragraph 1.1.1.2 might be wholly contained in the SBN edition on page 2.
+ Paragraph 1.1.1.3 might span two pages in the SBN edition, from page 2-3.

But a citation to the SBN edition may simply be:
>SBN 2

How should we credit paragraphs based on this particular citation?

Fortunately, we have a dictionary that links each paragraph to an SBN edition page range. The dictionary works by taking as input a paragraph and giving as output a page or page range. Call this the [Norton to SBN dictionary](./Norton to SBN Dictionary.txt).

Here’s how we can make use of such a dictionary to give credit to paragraphs in the Master Score List based on this citation to SBN 2:
+ First, it’s important to recognize that since this is just one citation, we have only 1 citation point to distribute to paragraphs in the Master Score List. So, whatever we do, we’re figuring out how to distribute this one point. This is similar to cases 2-4 above where we divided up the credit for a citation across multiple paragraphs.
+ Second, we take the page number for the citation and look up which SBN paragraphs it corresponds to in our Norton to SBN dictionary. That is, we look up which paragraphs include the page in the citation—in this case, 2—in their range of pages.
  + When we look up 2 in the dictionary, we find that 1.1.1.1, 1.1.1.2, and 1.1.1.3 each have page 2 in their range.
+ Third, we divide credit evenly between all of the paragraphs which have the relevant page number in their ranges. So, in this case, since 3 paragraphs contain page 2 in their ranges, each of them can be initially allotted 1/3 of the citation credit. In general, then, at this initial stage if there are n paragraphs on the page cited, each paragraph is allocated 1/n points thus far. Call this each paragraph’s **initial allotment**.
  + In our example, then, all of our paragraphs have an initial allotment of 1/3
+ Fourth, notice that paragraphs 1.1.1.1 and 1.1.1.3 aren’t wholly on page 2. To reflect that, let’s reduce their credit as follows. Each paragraph’s initial allotment can be reduced in proportion to how many pages that paragraph spans. So, if a paragraph spans two pages, its initial allotment is reduced by half. If it spans three pages, its initial allotment is reduced by a third. Generally, if a paragraph spans p pages, its initial allotment is reduced by 1/p. Call this number a paragraph’s **intermediate allotment**.
  + In our example, then:
    + 1.1.1.1 spans 2 pages and has an initial allotment of 1/3. Its initial allotment is reduced by 1/2. So, its intermediate allotment is 1/6.
    + 1.1.1.2 spans 1 page and has an initial allotment of 1/3. Its initial allotment is reduced by 1/1. So, its intermediate allotment is 1/3.
    + 1.1.1.3 spans 2 pages and has an initial allotment of 1/3. Its initial allotment is reduced by 1/2. So, its intermediate allotment is 1/6.
+ Fifth, we don’t want to increase each paragraph’s score in the Master Score List by its intermediate allotment. If we did, then each citation in an SBN citation would contribute less than 1 point overall to the Master Score List. For example, in our case so far, where the citation is to SBN 2, we would be increasing 1.1.1.1 by 1/6 point, 1.1.1.2 by 1/3 point, and 1.1.1.3 by 1/6 point. Overall, we would only be increasing the Master Score List by 2/3 point based on this citation. To correct for this, we can normalize the points so that they all add up to 1. To do that, we’ll add the intermediate allotments, divide 1 by that total, and multiply each intermediate total by this ratio to get our final allotment. Each paragraph then has its score in the Master Score List increased by its **final allotment**.
  + In our example, then, the intermediate allotments add up to 2/3. When we divide that by 1, we get 3/2. So, our final allotments in this example are calculated as follows:
   + 1.1.1.1 has an intermediate allotment of 1/6. 3/2 x 1/6 is 3/12 or 1/4 point. So, 1.1.1.1’s score in the Master Score List is increased by 1/4 point.
   + 1.1.1.2 has an intermediate allotment of 1/3. 3/2 x 1/3 is 1/2 point. So 1.1.1.2 has its score increased in the Master Score List by 1/2 point.
   + 1.1.1.3 has an intermediate allotment of 1/6. 3/2 x 1/6 is 3/12 or 1/4 point. So, 1.1.1.3’s score in the Master Score List is increased by 1/4 point.

The process described so far handles the simplest case of crediting paragraphs when a citation gives a single page in the SBN edition. However, there are cases when we will layer both kinds of complexity discussed so far. That is, citations to the SBN edition will not only be to single pages. They will sometimes be to page collections (e.g. SBN 14, 21, 89), or to page ranges (e.g. SB N 14-18), or to a collection of mixtures and ranges (e.g. SBN 14-18, 21, 88-90).

We handle these cases by combining the strategies for both types of complexity.
+ First, as we saw in cases 2-4 above, we convert page collections and ranges into a collection and then divide the citation credit evenly among members of the collection.
+ Second, as seen immediately above in converting single pages into paragraph citations, we follow the procedure for utilizing the Norton to SBN dictionary to distribute citations to a page across paragraphs on that page.
+ Third, increase the Master Score List of each paragraph by multiplying the results of the first part of this process (dividing the credit evenly among the pages in the collection) by the fractions resulting from the second part of this process (converting a single page into partial credit for paragraphs).

I'll work out an example below in detail. Suppose we are given the following citation:
>SBN 14-16, 21

First, we convert this complex citation which includes page ranges and single pages into a collection of pages:
>14, 15, 16, 21

Second, we convert page into a paragraph distribution. For illustration, I’ll copy out the page ranges from the Norton to SBN dictionary here and then use them to calculate the results of converting each page to a point distribution:

+ 1.1.5.1 : 13-14
+ 1.1.5.2 : 14
+ 1.1.5.3 : 14
+ 1.1.5.4 : 14
+ 1.1.5.5 : 14
+ 1.1.5.6 : 14-15
+ 1.1.5.7 : 15
+ 1.1.5.8 : 15
+ 1.1.5.9 : 15
+ 1.1.5.10 : 15
+ 1.1.6.1 : 15-16
+ 1.1.6.2 : 16
+ 1.1.7.7 : 20-21
+ 1.1.7.8 : 21
+ 1.1.7.9 : 21-22

So, for page 14:
- There are 6 paragraphs with page 14 in their range, 1.1.5.1-1.1.5.6. Each paragraph has an initial allotment of 1/6 point
- Paragraphs 1.1.5.1 and 1.1.5.6 each have two pages in their range, so their intermediate allotments are 1/12 while the rest remain at 1/6.
  + When we add up the totals, we find we have 5/6 points total. So, to get the final allotments for the paragraphs with page 14 in their range, we need to multiply each intermediate allotment by 6/5. So, the final allotments for the paragraphs tied to page 14 are as follows:
   - 1.1.5.1: 1/10 point
   - 1.1.5.2-5: 1/5 point
   - 1.1.5.6: 1/5 point

For page 15:
- There are again 6 paragraphs which have page 15 in their range, 1.1.5.6-1.1.6.1. The break down in terms of how many of those paragraphs have how many pages is exactly the same as for page 14—the first and last paragraphs tied to page 15 span 2 pages, the middle 4 span 15. So, the point distributions tied to page 15 will be as follows:
 + 1.1.5.6: 1/10 point
 + 1.1.5.7-10: 1/5 point
 + 1.1.6.1: 1/10 point

 For page 16:
 - There are 2 paragraphs that have page 16 in their range: 1.1.6.1, 1.1.6.2. So, the initial allotment of each is 1/2.
  + Paragraph 1.1.6.1 has two pages in its range. So, its intermediate allotment is 1/4 while 1.1.6.2 remains 1/2.
  + To get the final allotment of each, we need to multiply each intermediate allotment by 4/3. So, the final allotments for paragraphs tied to page 16 are as follows:
   - 1.1.6.1: 1/3 point
   - 1.1.6.2: 2/3 point

For page 21:
- There are three paragraphs which have page 21 in their range, 1.1.7.7, 1.1.7.8, 1.1.7.9. So, the initial allotment for each paragraph from page 21 is 1/3.
- Paragraphs 1.1.7.7 and 1.1.7.9 have 2 pages each in their range. So, their intermediate allotments are reduced by 1/2. So the intermediate allotments are 1/6 for 1.1.7.7 and 1.1.7.9 and 1/3 for 1.1.7.8.
- Finally, since the sum of intermediate allotments is 2/3, we calculate the final allotments to each paragraph from page 21 by multiplying intermediate allotments by 3/2. So, the final allotments from page 21 to paragraphs are as follows:
 + 1.1.7.7: 1/4 point
 + 1.1.7.8: 1/2 point
 + 1.1.7.9: 1/4 point

The total points added to each paragraph’s score on the Master Score List by this citation can be described by the following table, which multiplies each page’s distribution across paragraphs by 1/4 since the citation includes 4 pages.

+ 1.1.5.1 gets 1/10 of the share from page 14, page 14 gets 1/4 of the point from the Citation, no other page contributes to 1.1.5.1, so 1.1.5.1 gets its score on the Master Score List increased by 1/40 point from this citation.
+ 1.1.5.2 gets 1/5 of the share from page 14, page 14 gets 1/4 of the point from the Citation, no other page contributes to 1.1.5.2, so 1.1.5.2 gets its score increased on the Master Score List by 1/20.
+ The same goes for 1.1.5.3, 1.1.5.4, and 1.1.5.5.
+ 1.1.5.6 gets 1/10 of the share from page 14, page 14 gets 1/4 of the point from the Citation, so it gets 1/40 of a point from page 14. 1.1.5.6 gets 1/10 of the share from page 15 and page 15 gets 1/4 of the point from the Citation, so 1.1.5.6. gets 1/40 of a point added to its score from page 15. No other pages contribute to 1.1.5.6. So, 1.1.5.6 gets 1/20 of a point added to its score on the master list from this Citation.
+ 1.1.5.7 gets 1/5 of the share from page 15, page 15 gets 1/4 of the point from the Citation, no other page contributes to 1.1.5.7, so 1.1.5.7 gets its score increased on the Master Score List by 1/20.
+ The same goes for 1.1.5.8, 1.1.5.9, and 1.1.5.10 
+ 1.1.6.1 gets 1/10 of the share from page 15, page 15 gets 1/4 of the point from the Citation, so it gets 1/40 of a point from page 15. + 1.1.6.1 gets 1/3 of the share from page 16 and page 16 gets 1/4 of the point from the Citation, so 1.1.6.1. gets 1/12 of a point added to its score from page 16. No other pages contribute to 1.1.6.1. So, 1.1.6.1 gets .108 points added to its score on the master list from this Citation.
+ 1.1.6.2 gets 2/3 of the share from page 16, page 16 gets 1/4 of the point from the Citation, so 1.1.6.2 gets 1/6 of a point from page 16. No other pages contribute to 1.1.6.2 in this Citation, so, 1.1.6.2 gets 1/6 of a point added to its score on the Master Score List from this citation.
+ 1.1.7.7 gets 1/4 of the share from page 21, page 21 gets 1/4 of the point from the citation, so 1.1.7.7 gets 1/16 of a point from page 21. No other pages contribute to 1.1.7.7 from this Citation so this citation increases 1.1.7.7’s score on the Master Score List by 1/16 of a point.
+ The same goes for 1.1.7.9.
+ 1.1.7.8 gets 1/2 of the share from page 21, page 21 gets 1/4 of the point from the citation, so 1.1.7.8 gets 1/8 of a point from page 21. No other pages contribute to 1.1.7.8 from this Citation so this citation increases 1.1.7.8’s score on the Master Score List by 1/8 of a point.

All of these points sum to one point, makes sense given that we’re dividing the contribution of a single citation to the total. These calculations are represented in the table below. Each cell under a page represents the the page’s share multiplied by the paragraph’s share of that page. So the cell at 1.1.5.1, Page 14 = 1/4 (page 14’s share of the whole Citation) x 1/10 (paragraph 1.1.5.1’s share of page 14). We can sum each row to get the Citation’s total contribution to each paragraph’s total on the Master Score List, and we can sum the sum of each paragraph to get the total contribution of the Citation to the Master Score List (which should be 1).

While this is incredibly laborious to lay out step by step, and it is by far the most complex case to tabulate, it’s all relatively straightforward arithmetic to distribute credit from complex citations to the SBN edition to individual paragraphs. You can find the code that performs all of this in the [Master Function List](./master_function_list.py)

|          |   Page 14   |   Page 15   |   Page 16   |  Page 21   |  Paragraph Totals |
| -------- | ----------- | ----------- | ----------- | ---------- |  ---------------- |
| 1.1.5.1  |     .025    |             |             |            |  .025             |
| 1.1.5.2  |     .05     |             |             |            |  .05              |
| 1.1.5.3  |     .05     |             |             |            |  .05              |
| 1.1.5.4  |     .05     |             |             |            |  .05              |
| 1.1.5.5  |     .05     |             |             |            |  .05              |
| 1.1.5.6  |     .025    |     .025    |             |            |  .05              |
| 1.1.5.7  |             |     .05     |             |            |  .05              |
| 1.1.5.8  |             |     .05     |             |            |  .05              |
| 1.1.5.9  |             |     .05     |             |            |  .05              |
| 1.1.5.10 |             |     .05     |             |            |  .05              |
| 1.1.6.1  |             |     .025    |   .083      |            |  .1083            |
| 1.1.6.2  |             |             |   .167      |            |  .1667            |
| 1.1.7.7  |             |             |             |  .0625     |  .0625            |
| 1.1.7.8  |             |             |             |  .0125     |  .125             |
| 1.1.7.9  |             |             |             |  .0625     |  .0625            |
|          |             |             |             |  TOTAL:    |  1                |
