<div align="center">

# Tarot

_🔮 塔罗牌 🔮_

</div>

<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/blob/beta/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_tarot?color=blue">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2+-green">
  </a>
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/releases/tag/v0.3.0">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_tarot?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_tarot">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_tarot/beta?color=red">
  </a>
  
</p>

## 序

*“许多傻瓜对千奇百怪的迷信说法深信不疑：象牙、护身符、黑猫、打翻的盐罐、驱邪、占卜、符咒、毒眼、塔罗牌、星象、水晶球、咖啡渣、手相、预兆、预言还有星座。”——《人类愚蠢辞典》*

## 版本

v0.3.0

⚠ 适配nonebot2-2.0.0beta.2+

[更新日志](https://github.com/MinatoAquaCrews/nonebot_plugin_tarot/releases/tag/v0.3.0)

## 安装

1. 通过`pip`或`nb`安装；

    ⚠ 资源过大，pypi包不含`./resource`下所有资源；

2. 塔罗牌图片资源默认位于`./resource`下，设置`env`下`TAROT_PATH`更改资源路径，`CHAIN_REPLY`设置全局启用群聊转发模式，可通过命令修改：

    ```python
    TAROT_PATH="./data/tarot_resource"
    CHAIN_REPLY=false
    ```

3. 启动时，插件会自动下载repo中最新的`resource/tarot.json`文件至用户指定目录，塔罗牌牌阵及解读不一定随版本更新；

4. 图片资源可选择**不部署在本地**，占卜时会自动尝试从repo中下载缓存，但速度较慢。

    ⚠ 使用`raw.fastgit.org`进行加速。

## 命令

1. 占卜：[占卜/塔罗牌]；

2. [超管] 开启/关闭群聊转发模式：[开启|启用|关闭|禁用] 群聊转发，可降低风控风险。

## 资源说明

1. 韦特塔罗(Waite Tarot)包括22张大阿卡纳(Major Arcana)牌与权杖(Wands)、星币(Pentacles)、圣杯(Cups)、宝剑(Swords)各系14张的小阿卡纳(Minor Arcana)共56张牌组成，其中国王、皇后、骑士、侍从也称为宫廷牌(Court Cards)；

    ⚠ 资源中额外四张王牌(Ace)不在体系中，因此不会在占卜时用到，因为小阿卡纳中各系均有Ace牌，但可以自行收藏。

2. `tarot.json`中对牌阵，抽牌张数、是否有切牌、各牌正逆位解读进行说明。`cards`中对所有塔罗牌做了正逆位含义和资源路径的说明，塔罗牌存在正逆位之分；

3. 塔罗牌根据牌阵的不同有不同解读，同时也与问卜者的问题、占卜者的解读等因素相关，因此不存在所谓的解读方式正确与否。`cards`中的正逆位含义参考以下以及其他网络资源：

    - 棱镜/耀光塔罗牌中文翻译，中华塔罗会馆(CNTAROT)
    - [AlerHugu3s-PluginVoodoo](https://github.com/AlerHugu3s/PluginVoodoo/blob/master/data/PluginVoodoo/TarotData/Tarots.json)
    - [塔罗.中国](https://tarotchina.net/)
    - [塔罗牌](http://www.taluo.org/)
    - [灵匣](https://www.lnka.cn/)

    🤔 也可以说是作者的解读版本。

4. 牌面资源：[阿里云盘](https://www.aliyundrive.com/s/cvbxLQQ9wD5/folder/61000cc1c78a1da52ef548beb9591a01bdb09a79)；

    ⚠ 文件夹名称、大阿卡纳恶魔牌(The Devil)名称、权杖4名称、女皇牌(The Empress)名称有修改。

5. 关于切牌。单独一张切牌（或提示牌）在占卜中没有意义，原`v0.2.5`中`塔罗牌`命令与`占卜`合并。

## 本插件改自

1. [真寻bot插件库-tarot](https://github.com/AkashiCoin/nonebot_plugins_zhenxun_bot)

2. [HoshinoBot-tarot](https://github.com/haha114514/tarot_hoshino)
