# 主题 N：<主题名>（纵向 YYYY-YYYY）

> 蒸馏时间：YYYY-MM-DD | 方法：直接读取原始数据 + sender 验证
> 数据范围：<range> | 候选消息：<N> 条 | 关键 verbatim：<N> 条

---

## 特殊时期标注

- 特殊时期：
- 受影响判断：
- 处理方式：

---

## CONFLICT 状态

| CONFLICT | 当前状态 | 本主题处理 |
|---|---|---|
| CONFLICT-XXX | 🟡 待验证 | 本主题继续验证/无关/可关闭 |

---

## 筛选方法

- 使用脚本：`filter_by_theme.py`
- 关键词：
- 时间范围：
- 上下文窗口：
- 限制：关键词只做导航，不做定性。

---

## 纵向时间排列

| 时间 | 事件/表达 | source | sender | 备注 |
|---|---|---|---|---|
| YYYY-MM-DD |  |  | sender=me(已验证) |  |

---

## 洞察

### N-1 <洞察标题>

[洞察] <具体判断>

| 时间 | 内容 | sender |
|---|---|---|
| YYYY-MM-DD | "<克制引用>" | me(已验证) |

- 证据等级：verbatim/artifact/impression
- 模式类型：stable_trait / stage_state / special_period_response / relationship_triggered / pending_pattern
- 情境权重：time=<...>; relationship=<...>; body=<...>; event=<...>; medium=<...>
- 置信度：evidence=高/中/低；interpretation=高/中/低；stability=高/中/低
- 事实/解释/命名：fact=<...>; interpretation=<...>; temporary_name=<...>
- 可推翻条件：<什么证据、Correction 或替代解释会削弱此洞察>
- 用户语言：<用户自己的说法/待用户命名>
- 特殊期影响：无/有，说明
- 与上版本对比：新增/验证/修订/推翻
- CONFLICT 影响：新增/更新/关闭/无

---

## 与上版本/第一轮对比

| 维度 | 上版本判断 | 本主题发现 | 处理 |
|---|---|---|---|
|  |  |  | 新增/修订/推翻/验证 |

---

## 待用户复核

1. <需要用户确认的洞察>
2. <可能的 Correction>
3. <可关闭的 CONFLICT>
4. <需要用户重命名或确认是否为稳定特质的问题>

---

## 蒸馏器自评

- 是否逐条验证 sender：
- 是否过度依赖关键词：
- 是否排除特殊时期：
- 是否有偷懒/讨好：
- 本主题 Correction 风险：

---

*主题 N 蒸馏完成。等待用户复核后进入下一主题。*

