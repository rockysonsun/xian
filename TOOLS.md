# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 老仙自我保护机制

### 自动备份脚本
- **路径**: `scripts/backup-laoxian.sh`
- **功能**: 备份配置文件 + Git 提交 + 清理旧备份
- **用法**:
  ```bash
  ./scripts/backup-laoxian.sh
  ```

### 备份策略
1. 每次重要更新前执行备份脚本
2. 本地备份保留最近10个版本
3. 自动提交到 Git
4. 如有远程仓库，自动推送

### 备份内容包括
- IDENTITY.md (身份)
- USER.md (主人信息)
- MEMORY.md (长期记忆)
- SOUL.md (核心性格)
- AGENTS.md (工作指南)
- TOOLS.md (工具配置)
- HEARTBEAT.md (心跳任务)
- memory/ (历史对话)
- skills/ (技能)
