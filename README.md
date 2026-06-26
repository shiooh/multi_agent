# Multi Agent の更新アルゴリズムのシミュレーション

## Turkey's Hyperplane

- ランダムな法線ベクトルを 100回試して, はじめに見つかった適切な hyperplane の Agent が多いほうに, 固定長 10 だけ移動する (ver1)

結果：

<video src="out/visualizer_ver1.mp4" controls="true" width="300"></video>

- ランダムな法線ベクトルを 100回試して, その hyperplane が最も不均衡に Agents を分割するような法線ベクトルの方向に, 固定長 10 だけ移動する (ver2)

結果：

<video src="out/visualizer_ver2.mp4" controls="true" width="300"></video>

- ランダムな法線ベクトルを 100回試して, その hyperplane が最も不均衡に Agents を分割するような法線ベクトルの方向に, 指定長 step_length だけ移動する. step_length は はじめ 10 で, 毎回 0.9 倍にする. (ver3)

結果：

<video src="out/visualizer_ver3.mp4" controls="true" width="300"></video>

## Center point
- 知っている（自分を含む）点の集合に対し. 各点のTukey深度を計算し, 最も深い点に移動する. グラフは全域有効木を含むランダムなグラフとした.

結果：

<video src="out/visualizer_ver4.mp4" controls="true" width="300"></video>
