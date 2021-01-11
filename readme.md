### 基於 adb&python&opencv 的日版 FGO"自動化測試"工具

由一個大學資訊系讀了三年(大二轉系),快要畢業卻發現啥屁都沒學會的可撥學生撰寫,
估計 Bug 一堆就當作是一次 coding 練習吧,
移植自我剛開始學 python 時寫的台版 FGO BOT
台版:https://github.com/Zhen-Bo/Fgo-bot

---

#### 動機

目前大多數腳本都為手機 app,常常掛久了 bot 的 app 會直接卡死不動被系統強制關閉,
且大多數沒有在吃完指定蘋果樹後繼續等待體力且執行腳本的能力,都是吃完指定的蘋果數後就停止腳本(印象中)

---

#### 推薦環境

- bluestacks 4.250.1.1002(解析度 1280x720,240dpi,開啟 adb 連接)
- python 3.7.9
- opencv-python 4.2.0.32

---

#### 使用教學

首先把這個專案下載下來後解壓縮,並安裝 python
開啟 cmd 切換到此資料夾路靜候執行 pip install -r requirements.txt
安裝好後執行 python main.py 即可執行
!!!:fire::fire::fire:注意事項:fire::fire::fire:!!!
要確保你的戰鬥可以透過寶具三連或是任意普攻在 3T 內通關再使用這個腳本

---

#### 未來規劃(有生之年系列)

- [ ] 更新日版從者更換的模板圖片
- [ ] GUI 介面:joy:
- [ ] 使用 python-adb 而非 adb.exe
- [ ] 自動獲取助戰圖片
- [ ] 複數助戰支援
- [ ] 打包成 exe
- [x] 多解析度支援
      ~~多加一個專門持續對模擬器截圖的線程,而非要判斷時才像模擬器截圖(無意義)~~

---

#### 簡易說明

![](https://cdn.discordapp.com/attachments/702882288182099988/796951229238345728/-53_-_AlanWang_-_.JPG)
反正我是懶的打註解了,台版腳本那邊有
只求佛系理解程式碼,然後估計有一堆 bug,邏輯判斷寫的賊醜,可讀性也很差的東東~~(反正能跑就行)~~
本想做 GUI 介面結果被 tkinter 狠狠打臉,就把它放到 TODO list 了

---

#### 使用說明

- core 資料夾:放了一堆 bot 會用到的東西
  - adb 資料夾:放 adb.exe 的地方
  - images 資料夾:放圖片模板的地方
    - adb.py 圖/點擊/拖曳的 func
    - decoder.py:把使用者設定檔的 ini 轉換成 bot 的腳本格式
    - util.py:adb 控制物件並且做圖片的模板比對
    - auto.py:bot 的本體,所有邏輯判斷的地方
    - button.ini:FGO 介面按鈕位子儲存的地方(1280x720)
- UserData 資料夾:放使用者腳本及好友圖片的地方
  - config 資料夾:存放周回腳本
  - support 資料夾:存放好友圖的地方(請用 1280x720 的解析度對圖片進行裁切)
- main.py:程式本體

---

#### 腳本設定

- support
  - support:你存放在 UserData/support 資料夾中你要使用的好友圖片名稱(需要副檔名)
- ap_recover:吃蘋果選項
  - count:吃蘋果的數量
    - -1:自然回體
    - 任意數字:你要吃蘋果的數量
  - apple:你要吃蘋果的種類
    - au:金蘋果
    - ag:銀蘋果
    - sq:彩蘋果
- recover_time
  - recover_time:在確認你沒有足夠體力進關卡後,等待多少分鐘嘗試重進一次
- default_skill 開技能順序(從左至右執行)
  - battle1:第一回合開技能順序
  - battle2:第二回合開技能順序
  - battle3:第三回合開技能順序
- default_card:卡片選擇順序(從左到右選)
  - battle1:第一回合選卡
  - battle2:第二回合選卡
  - battle3:第三回合選卡

---

#### 開技格式

![](https://cdn.discordapp.com/attachments/702882288182099988/796963836585967656/unknown.png)

##### 從左至右分別為 a~i,如果該繼能不須指定從者,直接填入對應英文(小寫),如需指定則要在填入對象從者站位

##### 衣服技能則為 m 開頭,再來寫要開的技能是幾號,然後如果需要選擇對象則需再加填入對向站位

##### 換人技能則為"x",而非 m 開頭,x 後街需要更換的前牌從者站位 1~3,和後牌從者站位 1~3(對應:4~6)

E.x.
我如果需要先放術傻 1 技然後放莉莉絲 3 技,再放術傻 3 技指定給莉莉絲之後再開信長 1 技的話
對應代碼輸入為:gfi2a

---

#### 選卡格式

##### 站位 1~3 寶具對應 a-c

##### 第 1 張卡到第 5 張對應為 1~5

##### 如果選第幾張都沒差則填入 x 讓系統自動從 5 張中選

Ex.我如果開頭要開莉莉絲寶具.剩下兩張卡選哪張都無所謂
對應代碼輸入為:bxx

**!!! x 只能放在已經選擇的卡片後!!!
正確:1bx
正確:axx
正確:2xx
正確:xxx
錯誤:xa2->執行結果第一張先選從者 1 寶具,第 2 張為卡片 2.第三章為隨機決定**

---

#### 參考專案

[will7101/fgo-bot(Archived)](https://github.com/will7101/fgo-bot)
[Meowcolm024/FGO-Automata](https://github.com/Meowcolm024/FGO-Automata)
