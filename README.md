# Multi Agent の更新アルゴリズムのシミュレーション

## 実行方法

```bash
python simulate_multi_agent_robots.py
```
現在のままでは Safe Point 法のシミュレーションがされるが, "simulate_multi_agent_robots.py" の 39-45 行目をコメントアウトし, 28-36 行目をアンコメントすると Tukey's Hyperplane 法をシミュレーションできる.

また, そのほかの詳細な設定も"simulate_multi_agent_robots.py"上で設定できる.

## Center point
- 近傍の点の集合と、それらのランダムな凸結合点複数個に対し. 各点のTukey深度を計算し, 最も深い点に移動する. 

結果：

https://github.com/user-attachments/assets/39b1942d-f44e-4b56-b588-fc6c960b63dc

（完全グラフ）

https://github.com/user-attachments/assets/6ad01706-c0d8-47d0-b1f2-b4931830e4b9

（有向木を含み, 各ロボットの近傍の数が $N_i \leq (F_i+1)(d+1)$ を満たすグラフ）

https://github.com/user-attachments/assets/c85875f8-f231-46f6-9341-a6649c5a212f

（遅延あり）

## Tukey's Hyperplane

- ランダムな法線ベクトルを 100回試して, はじめに見つかった Tukey's Hyperplane の Agent が多いほうに, 固定長 10 だけ移動する (ver1)

結果：

https://github.com/user-attachments/assets/db12af38-7902-45c7-96fc-9f9a31b5ace7

（完全グラフ）

- ランダムな法線ベクトルを 100回試して, 見つけた Tukey's Hyperplane のうち最も不均衡に Agents を分割するものの法線ベクトルの方向に, 固定長 10 だけ移動する (ver2)

結果：

https://github.com/user-attachments/assets/d8cbf299-ea22-4c85-9fb0-5a71f3f8b0ea

（完全グラフ）

- ランダムな法線ベクトルを 100回試して, 見つけた Tukey's Hyperplane のうち最も不均衡に Agents を分割するものの法線ベクトルの方向に, 指定長 step_length だけ移動する. step_length は はじめ 10 で, 毎回 0.9 倍にする. (ver3)

結果：

https://github.com/user-attachments/assets/69aaa6d2-aedd-4e1e-844c-045255bb65a8

（完全グラフ）

https://github.com/user-attachments/assets/b37d011c-4150-497a-8dac-4534069c7a47

https://github.com/user-attachments/assets/d53e8cb4-e47b-4f09-af08-0b4a1f23e247

https://github.com/user-attachments/assets/7c30604a-3689-4e68-b146-bf1e5523bd05

（有向木を含み, 各ロボットの近傍の数が $N_i \leq (F_i+1)(d+1)$ を満たすグラフ = Centerpointアルゴリズムの条件と同様）
