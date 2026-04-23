# utils/shared.py
import os, io, re, json, itertools, platform
import numpy as np
import requests
import jieba
from PIL import Image
from collections import Counter

DOUBAO_API_KEY = "ark-45dee623-dd63-4749-b67e-b327ba49f8f1-64107"

# 项目根目录（绝对路径）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_default_font():
    # 1. 优先找项目根目录下 fonts/ 文件夹里的第一个字体
    fonts_dir = os.path.join(ROOT_DIR, "fonts")
    if os.path.exists(fonts_dir):
        for f in os.listdir(fonts_dir):
            if f.lower().endswith(('.ttf', '.otf', '.ttc')):
                return os.path.join(fonts_dir, f)
    # 2. 回退到系统字体
    if platform.system() == "Windows":
        paths = ["C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/msyh.ttc"]
    elif platform.system() == "Darwin":
        paths = ["/Library/Fonts/Arial Unicode.ttf", "/System/Library/Fonts/STHeiti Light.ttc"]
    else:
        paths = ["/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"]
    for p in paths:
        if os.path.exists(p): return p
    return "simhei.ttf"

def process_mask_to_array(image, threshold=240):
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        image = image.convert("RGBA")
        r, g, b, a = image.split()
        if a.getextrema()[0] < 255:
            mask = np.where(np.array(a) > 10, 0, 255).astype(np.uint8)
            return np.stack([mask]*3, axis=-1)
    img_array = np.array(image.convert("RGB"))
    min_channels = np.min(img_array, axis=2)
    mask = np.where(min_channels >= threshold, 255, 0).astype(np.uint8)
    return np.stack([mask]*3, axis=-1)

def call_ai_api(prompt):
    url = "https://ark.cn-beijing.volces.com/api/v3/responses"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DOUBAO_API_KEY}"}
    body = {
        "model": "doubao-seed-2-0-pro-260215",
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}]
    }
    res = requests.post(url, json=body, headers=headers, timeout=120)
    if res.status_code != 200:
        raise ValueError(f"文本API请求失败：{res.status_code}，{res.text}")
    data = res.json()
    try:
        if "output" in data and "text" in data["output"]: return data["output"]["text"]
        elif "choices" in data: return data["choices"][0]["message"]["content"]
        else: return str(data)
    except Exception:
        raise ValueError(f"API 返回格式异常：{data}")

def ai_match_mask_filename(text, candidate_files):
    if not candidate_files: raise ValueError("masks 文件夹为空。")
    prompt = f"""你是一个严格遵守规则的助手。请从给定列表中挑一个与文本最相近的文件名。
文本：{text}
候选列表：{candidate_files}
规则：只返回一个文件名，不要加引号或任何说明。"""
    result = call_ai_api(prompt).strip().strip('"').strip("'")
    if result in candidate_files: return result
    for f in candidate_files:
        if f == result or f in result or result in f: return f
    raise ValueError(f"AI 未返回有效文件名：{result}")

def generate_mask_image_by_ai(text):
    drawing_prompt = f"""请根据以下文本内容提取最能概括其核心概念的具体物品或形状进行作画。
文本内容：{text[:1000]}
生成要求（必须严格遵守）：
1. 本图像将作为国际顶刊（如Nature/Cell）专业学术论文的词云掩码（Mask），必须极度专业、严谨、大方、高级。
2. 必须是高度抽象概括的极简实心纯黑剪影（Silhouette）。无内部细节、无灰度过渡、无边框、无阴影、无文字，背景必须完全纯白，主体必须完全纯黑。
3. 允许根据文本概念生成多个主体（例如"脑肠轴"可以同时出现大脑和肠道），但它们必须在视觉上构成一个协调、连贯、紧凑的整体轮廓。坚决杜绝生硬拼接、散乱分布、像劣质插画一样的排版，绝对不要使用细劣的线条、箭头或关系连接符。
4. 整体外轮廓必须平滑流畅，作为词云背景形状时能保持视觉上的饱满感与图形美感。
"""
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DOUBAO_API_KEY}"}
    body = {"model": "doubao-seedream-5-0-260128", "prompt": drawing_prompt, "response_format": "url"}
    res = requests.post(url, json=body, headers=headers, timeout=120)
    if res.status_code != 200:
        raise ValueError(f"AI生图失败，HTTP状态码：{res.status_code}，响应内容：{res.text}")
    data = res.json()
    try:
        image_url = data["data"][0]["url"]
    except Exception:
        raise ValueError(f"解析生图URL失败。API返回：{data}")
    img_res = requests.get(image_url, timeout=120)
    img_res.raise_for_status()
    return Image.open(io.BytesIO(img_res.content))

def generate_vosviewer_json(text_data, selected_words_dict):
    import math
    word_to_id = {word: idx + 1 for idx, word in enumerate(selected_words_dict.keys())}
    items = []
    golden_ratio = (1 + math.sqrt(5)) / 2
    angle_increment = math.pi * 2 * golden_ratio
    for idx, (word, wid) in enumerate(word_to_id.items()):
        r = math.sqrt(idx + 1) * 15
        theta = idx * angle_increment
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        items.append({
            "id": wid, "label": word,
            "x": round(x, 2), "y": round(y, 2),
            "cluster": (idx % 7) + 1,
            "weights": {"Frequency": selected_words_dict[word]}
        })
    sentences = re.split(r'[。！？.!?\n]+', text_data)
    links_dict = {}
    for sentence in sentences:
        if not sentence.strip(): continue
        words_in_sentence = list(set([w for w in jieba.lcut(sentence) if w in word_to_id]))
        if len(words_in_sentence) >= 2:
            for w1, w2 in itertools.combinations(words_in_sentence, 2):
                id1, id2 = word_to_id[w1], word_to_id[w2]
                if id1 > id2: id1, id2 = id2, id1
                links_dict[(id1, id2)] = links_dict.get((id1, id2), 0) + 1
    links = [{"source_id": id1, "target_id": id2, "strength": weight}
             for (id1, id2), weight in links_dict.items()]
    return json.dumps({"network": {"items": items, "links": links}}, ensure_ascii=False, indent=2)
