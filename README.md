# シミュレーション

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

- ビジュアライザーを改良(ver4)

結果：

<video src="out/visualizer_ver4.mp4" controls="true" width="300"></video>
