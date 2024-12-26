# Buckshot Roulette CLI(dev.)

## Introduction

Buckshot Roulette in CLI

A CLI implementation of Mike Klubnika's Buckshot Roulette game.

Original Author : Mike Klubnika

Still Developing & debuging, create an issue if you found a bug.(Simplified Chinese is preferred, followed by English)

## 简介

《恶魔轮盘》命令行版

Mike Klubnika的《恶魔轮盘》游戏的命令行界面实现

原作者: Mike Klubnika

目前仍在开发和debuging，可能存在bug，欢迎发issue（优先使用简体中文，其次是英语）

## Requirements

Python3 required, minimum supported version not tested, possibly >=3.8.

rich`[>=13.8.0]` required ,install it by this command.

    `pip install rich`

or install a specifying version.

    `pip install rich==13.8.0`

You may use `pip3` instead of `pip` on macOS/Linux.

Besides, your terminal should support Emoji display, basically all supported on Windows/macOS/Linux over SSH and terminal on GUI.

## 依赖

需要Python3，未测试具体版本，应该要求Python3.8及以上版本

需要rich`[>=13.8.0]`库，通过以下命令安装：

    `pip install rich`

或者安装指定版本。

    `pip install rich==13.8.0`

在macOS和Linux上，你可能需要用`pip3`命令而不是`pip`。

另外，你的终端需要支持emoji显示，现在Windows/macOS/通过SSH连接的Linux命令行和Linux图形界面下的终端基本上都已支持。

## Emoji supported terminal/支持emoji的终端

    ✅：Support/支持
    ❌: Unsupport/不支持
    ⚠️：Support but have display problem/支持，但存在显示问题

| 💻 | ❓ |
| ----------- | ----------- |
| MobaXterm | ⚠️ |
| Xshell | ⚠️ |
| Termux | ✅ |
| Termius | ✅ |
| bash | ✅ |
| zsh | ✅ |
| zsh(macOS) | ✅ |
| Windows Terminal(Windows 11) | ✅ |
| cmd.exe | ⚠️ |
| CLI tty | ❌ |
| PuTTY | ⚠️ |

You may install emoji fonts or install `fonts-noto-color-emoji` package or `noto-fonts-emoji` package on Linux.

在Linux，你可能需要安装emoji字体或者安装`fonts-noto-color-emoji`或者`noto-fonts-emoji`


## 玩法

与原作玩法基本一致。

[简体中文 : 游民星空](https://www.gamersky.com/handbook/202404/1728981.shtml)

## How to play

Basically the same as the original game.

[English : Wikipedia](https://en.wikipedia.org/wiki/Buckshot_Roulette)

## Can I change Game Language?

Editing `gameConfig.py` to change game language or modify game setting according to config file comments.

You can also modify/create a language translation file `language_*LOCALECODE*.py`.

## 切换游戏语言

你可以编辑`gameConfig.py`，根据注释提示切换游戏语言或修改其他设置。

你可以修改/创建语言翻译文件`language_*LOCALECODE*.py`。

## I'am ready to play!

    `python br.py`

or

    `python3 br.py`

## 开始游戏

    `python br.py`

或者

    `python3 br.py`