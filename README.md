<div align="center">

# Tarot

_ð® å¡ç½ç ð®_

</div>

<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/blob/beta/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_tarot?color=blue">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2+-green">
  </a>
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/releases/tag/v0.3.3">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_tarot?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_tarot">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_tarot/beta?color=red">
  </a>
  
</p>

## åº

*âè®¸å¤å»çå¯¹åå¥ç¾æªçè¿·ä¿¡è¯´æ³æ·±ä¿¡ä¸çï¼è±¡çãæ¤èº«ç¬¦ãé»ç«ãæç¿»ççç½ãé©±éªãå åãç¬¦åãæ¯ç¼ãå¡ç½çãæè±¡ãæ°´æ¶çãåå¡æ¸£ãæç¸ãé¢åãé¢è¨è¿ææåº§ãâââãäººç±»æè ¢è¾å¸ã*

## çæ¬

v0.3.3

â  éénonebot2-2.0.0beta.2+

[æ´æ°æ¥å¿](https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/releases/tag/v0.3.3)

## å®è£

1. éè¿`pip`æ`nb`å®è£ï¼

    â  èµæºè¿å¤§ï¼pypiåä¸å«`./resource`ä¸ææå¡ç½çå¾çèµæºï¼

2. å¡ç½çå¾çèµæºé»è®¤ä½äº`./resource`ä¸ï¼è®¾ç½®`env`ä¸`TAROT_PATH`æ´æ¹èµæºè·¯å¾ï¼`CHAIN_REPLY`è®¾ç½®å¨å±å¯ç¨ç¾¤èè½¬åæ¨¡å¼ï¼å¯éè¿å½ä»¤ä¿®æ¹ï¼

    ```python
    TAROT_PATH="./data/path-to-your-resource"
    CHAIN_REPLY=false
    ```

3. å¯å¨æ¶ï¼æä»¶ä¼èªå¨ä¸è½½repoä¸­ææ°ç`resource/tarot.json`æä»¶è³ç¨æ·æå®ç®å½ï¼å¡ç½ççéµåè§£è¯»ä¸ä¸å®éæä»¶çæ¬æ´æ°ï¼

4. å¾çèµæºå¯éæ©**ä¸é¨ç½²å¨æ¬å°**ï¼å åæ¶ä¼èªå¨å°è¯ä»repoä¸­ä¸è½½ç¼å­ã

    â  ä½¿ç¨`raw.fastgit.org`è¿è¡å éï¼ä¸ç¡®ä¿æ¬¡æ¬¡æå

## å½ä»¤

1. å åï¼[å å]ï¼

2. å¾å°åå¼ å¡ç½çååºï¼[å¡ç½ç]ï¼

3. [è¶ç®¡] å¼å¯/å³é­ç¾¤èè½¬åæ¨¡å¼ï¼[å¼å¯|å¯ç¨|å³é­|ç¦ç¨] ç¾¤èè½¬åæ¨¡å¼ï¼å¯éä½é£æ§é£é©ã

## èµæºè¯´æ

1. é¦ç¹å¡ç½(Waite Tarot)åæ¬22å¼ å¤§é¿å¡çº³(Major Arcana)çä¸ææ(Wands)ãæå¸(Pentacles)ãå£æ¯(Cups)ãå®å(Swords)åç³»14å¼ çå°é¿å¡çº³(Minor Arcana)å±56å¼ çç»æï¼å¶ä¸­å½çãçåãéªå£«ãä¾ä»ä¹ç§°ä¸ºå®«å»·ç(Court Cards)ï¼

    â  èµæºä¸­é¢å¤åå¼ çç(Ace)ä¸å¨ä½ç³»ä¸­ï¼å æ­¤ä¸ä¼å¨å åæ¶ç¨å°ï¼å ä¸ºå°é¿å¡çº³ä¸­åç³»åæAceçï¼ä½å¯ä»¥èªè¡æ¶èã

2. `tarot.json`ä¸­å¯¹çéµï¼æ½çå¼ æ°ãæ¯å¦æåçãåçæ­£éä½è§£è¯»è¿è¡è¯´æã`cards`ä¸­å¯¹ææå¡ç½çåäºæ­£éä½å«ä¹åèµæºè·¯å¾çè¯´æï¼å¡ç½çå­å¨æ­£éä½ä¹åï¼

3. å¡ç½çæ ¹æ®çéµçä¸åæä¸åè§£è¯»ï¼åæ¶ä¹ä¸é®åèçé®é¢ãå åèçè§£è¯»ç­å ç´ ç¸å³ï¼å æ­¤ä¸å­å¨æè°çè§£è¯»æ¹å¼æ­£ç¡®ä¸å¦ã`cards`ä¸­çæ­£éä½å«ä¹åèä»¥ä¸ä»¥åå¶ä»ç½ç»èµæºï¼

    - æ£±é/èåå¡ç½çä¸­æç¿»è¯ï¼ä¸­åå¡ç½ä¼é¦(CNTAROT)
    - [AlerHugu3s-PluginVoodoo](https://github.com/AlerHugu3s/PluginVoodoo/blob/master/data/PluginVoodoo/TarotData/Tarots.json)
    - [å¡ç½.ä¸­å½](https://tarotchina.net/)
    - [å¡ç½ç](http://www.taluo.org/)
    - [çµå£](https://www.lnka.cn/)

    ð¤ ä¹å¯ä»¥è¯´æ¯ä½èçè§£è¯»çæ¬

4. çé¢èµæºï¼[é¿éäºç](https://www.aliyundrive.com/s/cvbxLQQ9wD5/folder/61000cc1c78a1da52ef548beb9591a01bdb09a79)ï¼

    â  æä»¶å¤¹åç§°ãå¤§é¿å¡çº³æ¶é­ç(The Devil)åç§°ãææ4åç§°ãå¥³çç(The Empress)åç§°æä¿®æ¹

## æ¬æä»¶æ¹èª

1. [çå¯»botæä»¶åº-tarot](https://github.com/AkashiCoin/nonebot_plugins_zhenxun_bot)

2. [HoshinoBot-tarot](https://github.com/haha114514/tarot_hoshino)
