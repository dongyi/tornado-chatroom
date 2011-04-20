

API: http://open.t.sina.com.cn/wiki

目前支持的接口

1.  登录/OAuth接口

    * oauth
    * oauth/request_token
    * oauth/authorize
    * oauth/access_token 

2.  获取下行数据集(timeline)接口

    * statuses/public_timeline 获取最新更新的公共微博消息
    * statuses/friends_timeline 获取当前用户所关注用户的最新微博信息 (别名: statuses/home_timeline)
    * statuses/user_timeline 获取用户发布的微博信息列表
    * statuses/mentions 获取@当前用户的微博列表
    * statuses/comments_timeline 获取当前用户发送及收到的评论列表
    * statuses/comments_by_me 获取当前用户发出的评论
    * statuses/comments 获取指定微博的评论列表
    * statuses/counts 批量获取一组微博的评论数及转发数
    * statuses/unread 获取当前用户未读消息数 

3.  微博访问接口

    * statuses/show 根据ID获取单条微博信息内容
    * user/statuses/id 根据微博ID和用户ID跳转到单条微博页面
    * statuses/update 发布一条微博信息
    * statuses/upload 上传图片并发布一条微博信息 
    * statuses/destroy 删除一条微博信息
    * statuses/repost 转发一条微博信息（可加评论）
    * statuses/comment 对一条微博信息进行评论
    * statuses/comment_destroy 删除当前用户的微博评论信息
    * statuses/reply 回复微博评论信息 

4.  用户接口

    * users/show 根据用户ID获取用户资料（授权用户）
    * statuses/friends 获取当前用户关注对象列表及最新一条微博信息
    * statuses/followers 获取当前用户粉丝列表及最新一条微博信息 

5.  私信接口

    * direct_messages 我的私信列表
    * direct_messages/sent 我发送的私信列表
    * direct_messages/new 发送私信
    * direct_messages/destroy 删除一条私信 

6.  关注接口

    * friendships/create 关注某用户
    * friendships/destroy 取消关注
    * friendships/exists 是否关注某用户(推荐使用friendships/show)
    * friendships/show 是否关注某用户 

7.  Social Graph接口
    * friends/ids 关注列表
    * followers/ids 粉丝列表 

8.  账号接口

    * account/rate_limit_status 获取当前用户API访问频率限制
    * account/update_profile_image 更改头像 

9.  收藏接口

    * favorites 获取当前用户的收藏列表
    * favorites/create 添加收藏
    * favorites/destroy 删除当前用户收藏的微博信息 

2010-09-06更新内容

1. 更改命名： twitter --> weibopy

2. UnicodeEncodeError时，需要encode('utf-8')编码


2010-08-19更新内容

1. simplejson：用于python2.4用户JSON解析支持包

2. 增加basicAuth验证方式
	示例：
	test = Test()
	test.basicAuth('consumer_key', 'username', 'password')
	test.update("test-测试")

3. 完善接口：
    * statuses/upload 上传图片并发布一条微博信息
    * account/rate_limit_status 获取当前用户API访问频率限制
    * account/update_profile_image 更改头像 
    * favorites 获取当前用户的收藏列表
    * favorites/create 添加收藏
    * favorites/destroy 删除当前用户收藏的微博信息 

4. 完善接口一对一示例：详见sinatpy.simplejson包


