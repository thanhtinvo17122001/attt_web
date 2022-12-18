import requests
from bs4 import BeautifulSoup
from app.modules.categories import categories_service
from app.modules.posts import posts_service
from app.modules.tags import tags_service
from app.common.helper import find_nth
from datetime import datetime, timedelta

def run():
  url = 'https://antoanthongtin.gov.vn'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  # Lấy tất cả danh mục con
  # all menus excludes menus has children
  menus = soup.select('.menuMain-top ul li:not(.has-sub) > a')
  # Tất cả link của các danh mục con
  category_links = [menu.attrs['href'] for menu in menus]

  # Lặp tất cả danh mục
  for category_link in category_links:
    if category_link == '/': continue
    # if category_link == '/chinh-tri---xa-hoi': break
    print('>>>>>>>>>>>> Crawling for category: ' + category_link + '\n')

    # all posts from a category
    all_post_links = []
    page_category_link = category_link
    # Lấy tất cả bài viết ở nhiều trang
    while True:
      categoryPage = requests.get(url + page_category_link)
      soup = BeautifulSoup(categoryPage.content, "html.parser")
      posts = soup.select('.newsCol-list ul li')
      all_post_links += [
        {
          'link': post.find('a').attrs['href'],
          'img': post.find('img').attrs['src']
        } for post in posts
      ]

      # has next page
      more_button = soup.select_one('.boxNewsL a.viewMore')
      if (more_button): page_category_link = more_button['href']
      else: break

    print('>>>>>>>>>>>> Crawling ', len(all_post_links), ' posts...')
    category = categories_service.find_one(slug=category_link[1:])

    # all_post_links: tất cả link của 1 danh mục
    for post in all_post_links:
      slug = post['link'][(find_nth(post['link'], '/', 2) + 1):]
      exist_post = posts_service.find_one(slug=slug)
      if exist_post: continue

      postPage = requests.get(url + post['link'])
      soup = BeautifulSoup(postPage.content, "html.parser")
      # Lấy title
      title_dom = soup.select_one('.newsDetail > h1')

      print('----------------------------------------------------------------------------------------------------')
      # Has post
      if title_dom:
        print(title_dom.text)
        # Lấy mô tả
        description = soup.select_one('.news-Content > div > strong').text.strip()
        # Nội dung
        content = str(soup.select_one('.news-Content .txtNews'))
        # Tác giả
        author = str(soup.select_one('.news-Content #tacgia'))
        # Ảnh bài viết
        thumbnail = post['img']
        # Giờ tạo bài viết
        # Get time UTC+7
        time = soup.select_one('.time-topic')
        hh = time.text[:time.text.find('|')].strip()
        ddmmyyyy = time.text[(time.text.find('|') + 2):find_nth(time.text, '|', 2)].strip()
        created_time = (datetime.strptime(hh + ' ' + ddmmyyyy, '%H:%M %d/%m/%Y') - timedelta(hours=7))

        tags = soup.select('.tagBox ul li a')
        all_tag_links = [
          {
            'slug': tag.attrs['href'][(find_nth(tag.attrs['href'], '/', 2) + 1):],
            'name': tag.text.capitalize(),
          }
          for tag in tags
        ]

        # Danh sách từ khoá
        tag_ids = []
        for item in all_tag_links:
          tag = tags_service.find_one(slug=item['slug'])
          if (tag is None):
            try:
              tag = tags_service.insert(
                slug=item['slug'],
                name=item['name'],
              )
            except:
              print("An exception occurred")
          if (tag):
            tag_ids.append(tag.id)

        tag_json = [id.hex for id in tag_ids]
        # Insert thông tin vào Database
        try:
          posts_service.insert(
            category_id=category.id,
            slug=slug,
            title=title_dom.text,
            description=description,
            thumbnail=thumbnail,
            content=content+author,
            view_count=100,
            created_at=created_time,
            updated_at=created_time,
            tag_ids=tag_json
          )

        except:
          print("An exception occurred")
      # break