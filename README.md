# Manubot Catalog

[![Travis CI Build Status](https://travis-ci.com/manubot/catalog.svg?branch=master)](https://travis-ci.com/manubot/catalog)

Manubot is a workflow and set of tools for the next generation of scholarly publishing.
Learn more at <https://manubot.org/>.

This repository stores a catalog of manuscripts that were made using Manubot.
These manuscripts are displayed at <https://manubot.org/catalog/>.
The `catalog.json` file produced by this codebase is available at `https://manubot.github.io/catalog/catalog.json`.

## Contributing

We encourage anyone to add manuscripts to the catalog.
In-progress manuscripts are acceptable.
Basically, any manuscript that has a substantial amount of content that is not part of [Rootstock](https://manubot.github.io/rootstock/) is of interest.

GitHub repositories containing Manubot manuscripts can be found with [this search](https://github.com/search?o=desc&q=manubot+in%3Areadme&s=updated&type=Repositories).

To add a manuscript to the catalog, add a record in [`catalog.yml`](catalog.yml).
`catalog.yml` is a YAML formatted file.
An example manuscript with documentation comments is below:

```yaml
- repo_url: https://github.com/greenelab/deep-review  # URL to GitHub repository with Manuscript source code
  html_url: https://greenelab.github.io/deep-review/  # URL for Manubot HTML output (usually hosted by GitHub Pages)
  thumbnail_url: https://url_for_image.png  # optional: square image to represent the manuscript. Overrides thumbnail set by manuscript.
  preprint_citation: doi:10.1101/142760  # optional: Manubot-style citation for a preprint corresponding to the manuscript
  journal_citation: doi:10.1098/rsif.2017.0387  # optional: Manubot-style citation for a published article corresponding to the manuscript
```

For more information on how to create citations for `preprint_citation` and `journal_citation`, see Manubot's citation-by-identifier [documentation here](https://github.com/manubot/rootstock/blob/main/USAGE.md#citations).
Specifying `thumbnail_url` overrides the thumbnail image detected from the metadata of `html_url`.
Therefore, setting `thumbnail_url` is only neccessary if the manuscript does not supply a thumbnail image or if the catalog should use a different image.

## Thumbnail Guidelines

Follow these guidelines when creating your thumbnail to help us maintain a beautiful, consistent, and streamlined catalog.
They are listed roughly in order of most strict to least strict.

*Click on the arrows/triangles to show more details about the guideline.*

<details>
<summary>
Size dimensions to 1000 × 1000 pixels
</summary>

Provide an image exactly 1000 pixels wide by 1000 pixels high.
Why do we ask for such a large image when the thumbnails of the papers appear so small in the catalog?

1. Web browsers can use the extra pixels to display a crisper image when zoomed in (especially important on high dpi displays).
2. The layout/design of the catalog is subject to change, which may show the thumbnails at larger sizes.
3. In general, we want to future-proof the catalog against increasing image resolution standards, and for Manubot's own changing needs.
</details>


<details>
<summary>
Use PNG format
</summary>

Provide your image as a `.png` file.
This avoids unsightly artifacts produced by other common image formats while still keeping file size to a minimum.
</details>


<details>
<summary>
Select a striking image
</summary>

Select a portion of your manuscript that is interesting and unique.
Your thumbnail is not expected to accurately capture or explain what your manuscript is about.
The purpose of the thumbnail is to visually distinguish your paper from other papers, so that readers can easily remember and quickly identify it among many others.
As such, the first preference is for a unique, colorful figure, without its caption.
If your manuscript has no figures, use an interesting-looking table, code block, or set of equations.
If your manuscript has none of those, use any other section that looks unique in some way; more than just a paragraph of black text.
If your manuscript is all just plain text, don't provide a thumbnail at all; a placeholder thumbnail will be used automatically.
</details>


<details>
<summary>
Don't stretch
</summary>

Don't distort the original aspect ratio of your image; not even a little.
It looks bad and is very noticeable.
Asymmetrical horizontal and vertical whitespace is much preferable to a stretched image.
If you are struggling to meet the dimension requirement, refer to the guidelines on cropping.
</details>


<details>
<summary>
Don't scale
</summary>

You should always create, save, and maintain your figures in vector format where possible.
This allows the image to be scaled to any size without loss of quality.
If your thumbnail source is a vector image, scale it to the required dimensions *before* converting/rendering it to `.png`.
Do not, for example, render your vector image to a 800×800 `.png` and then scale it up to 1000×1000.
If your thumbnail has to be a raster image, it still must meet the dimension requirements above, and may be rejected by the catalog maintainers if it is noticeably up-scaled.
</details>


<details>
<summary>
Use a solid background
</summary>

If your image has any transparent/translucent areas, place a background behind it.
Solid backgrounds are strongly preferred.
White is the first preference, but if it is necessary to use a different color to achieve adequate contrast, we ask that you follow the [Manubot style guidelines](https://github.com/manubot/resources/blob/main/brand/readme.md#style-guidelines) to the best of your ability.
</details>


<details>
<summary>
Don't include paragraph text or captions
</summary>

Text, especially plain black text, serves little to no purpose in a thumbnail.
Thumbnails are meant to be quick visual identifiers, not snippets of detailed content.
Don't include text in your thumbnail, unless it is baked into the figure itself (not its caption), or unless it is necessary per the "striking image" guideline above.
</details>


<details>
<summary>
Frame/crop nicely
</summary>

Cropping an image nicely is more of an artform than you might think.
As such, it's hard to specify a set of hard/quantifiable rules about what looks good.
If you're familiar with [frame composition](https://en.wikipedia.org/wiki/Composition_(visual_arts)) from art/photography/cinematography, the same techniques can be applied here.
In addition, here are some general guidelines to follow:
<blockquote>
<details>
<summary>
Choose a good aspect ratio
</summary>

Since our dimension requirements are a square, figures that are square or close to square will look the best.
Figures with an aspect ratio greater than 3:1 (width:height or height:width) should be avoided.
For example, a figure that is more than three times taller than it is wide might not be the best choice for a thumbnail.
</details>
<details>
<summary>
Center horizontally and vertically
</summary>

Centering an image horizontally and vertically tends to look the best.
But be careful: sometimes making the space on either side exactly the same actually doesn't look centered to the human eye.
Consider a typical play button icon, a rightward-pointing triangle.
Its center of mass is slightly to the left, and needs to be moved slightly right of true-center to look naturally-centered.
Take into account the "center of mass" of your figure.
</details>
<details>
<summary>
Use ~50px of padding
</summary>

Where it is possible to contain your whole figure in the bounds of the image, keep about 50px of space between the content of the figure and each boundary of the image.
If your figure has to extend beyond the vertical boundaries of the image, leave this much horizontal padding, and vice versa.
In general, on any side that you're cutting through white-space, leave this much padding.
</details>
<details>
<summary>
Cut through white-space
</summary>

Don't cut through text or other significant objects at the borders of your image.
If it is absolutely necessary to do so, choose the cut point with care.
Cutting through the center or quarter-waypoint of an object looks better than -- for example -- leaving a stray, unintentional-looking 3 pixels of it protruding into the image.
If a small protrusion like that is absolutely necessary, it's okay to simply white it out and make it blank space.
</details>
</blockquote>
</details>


<details>
<summary>
Use good contrast
</summary>

Your thumbnail may be viewed at different sizes and on different screens.
It is important that anyone can see clearly defined shapes in your image, even at a small size.
Make sure the key edges and outlines of your objects are sharp and readable.
Do not use colors that are close together.
Avoid hard to read combinations like white and yellow.
</details>


<details>
<summary>
Don't show plugins (irrelevant if submitting a figure directly)
</summary>

Don't show Manubot or third party plugins in your thumbnail.
The purpose of the thumbnail is to represent your particular paper, not to showcase features of Manubot (there are other places for that).
In particular, be mindful to remove the Hypothesis side toolbar, Hypothesis highlights, the table of contents panel, and any open tooltips.
</details>
<details>
<summary>
Don't show theme decorations (irrelevant if submitting a figure directly)
</summary>

Some Manubot themes show a subtle page border and shadow, meant to represent an actual sheet of paper.
Don't include these in your thumbnails, or any other theme decoration that will add clutter to the image in its final context.
For example, our catalog already adds a shadow around the thumbnails, and it would look bad to have another shadow within the image itself.
These types of effects are intended to be "sugar"/embellishment for the html version of manuscripts only.
They're not considered core to the content and functionality of the paper, and thus don't belong in a thumbnail.
They are also more likely to change as web design trends change.
In general, if a piece of styling is stripped away when printing your manuscript, don't include it in your thumbnail.
</details>
<details>
<summary>
Use default theme, without modifications (irrelevant if submitting a figure directly)
</summary>

To keep the catalog thumbnails consistent, we prefer that you use the default Manubot theme when creating your thumbnail.
We also strongly prefer you make no modifications to the theme, to ensure that sizing and spacing of elements on the page are all in-line with best-practices of graphic design.
</details>


_**When in doubt, look at the other thumbnails and model yours after them.**_
