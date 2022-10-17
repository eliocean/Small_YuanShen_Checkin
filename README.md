# Simple_YuanShen_Checkin
## YuanShen 每日签到小脚本，参考:  

- **[genshinhelper2](https://github.com/y1ndan/genshinhelper2)**



## 使用方法

- 方法一：获取cookie 放到 `checkin/COOKIE` 文件中

- 方法二：获取cookie 放到 [github本项目]:`Settings-Secrets-Actions `中，创建(或更新)名为`COOKIE` 的secret。 


## 获取米游社Cookie

1. 打开你的浏览器,进入**无痕/隐身模式**

2. 由于米哈游修改了bbs可以获取的Cookie，导致一次获取的Cookie缺失，所以需要增加步骤

3. 打开`http://bbs.mihoyo.com/ys/`并进行登入操作

4. 在上一步登入完成后新建标签页，打开`http://user.mihoyo.com/`并进行登入操作 (如果你不需要自动获取米游币可以忽略这个步骤，并把`mihoyobbs`的`enable`改为`false`即可)

5. 按下键盘上的`F12`或右键检查,打开开发者工具,点击Console

6. 输入

   ```javascript
   var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}
   ```

   回车执行，并在确认无误后点击确定。

7. **此时Cookie已经复制到你的粘贴板上了**
