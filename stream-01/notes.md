


# Arby's Restaurant Scraper : We Have The MEAT



**URLS**
-  https://locations.arbys.com/index.html (State Index)
-  https://locations.arbys.com/al.html (Township Index)
-  https://locations.arbys.com/al/alabaster.html (Proximity ID)



## Get States

**HTML For state based index**
- https://locations.arbys.com/index.html


  ```HTML
  <div class="container state-list-container">
    <h1 class="state-list-title">Arby's locations:</h1>
    <div class="state-list-usa">
      <div class="state-list-usa-title">United States</div>

    <div class="c-directory-list"><div class="c-directory-list-content-wrapper">
      <ul class="c-directory-list-content">
        <li class="c-directory-list-content-item">
          <a class="c-directory-list-content-item-link" href="al.html" data-yext-tracked="true">Alabama</a>

          .....

        </li><li class="c-directory-list-content-item">
          <a  class="c-directory-list-content-item-link" href="wy.html" data-yext-tracked="true">Wyoming</a>
        </li>
      </ul></div></div></div>
  </div>


  ```
  - Scrape the href `class="c-directory-list-content-item-link"` inside `class="state-list-container"`


**Note:**
Some locations may include direct pages to an arby's because of a limited number in that area. To ensure we get all of the restaurants, we will identify any direct links and save them in a list, then parse the list of all direct links at the end

## Get Townships


``` HTML
<a class="c-directory-list-content-item-link" href="al/alabaster.html" data-yext-tracked="true">Alabaster</a>

```
