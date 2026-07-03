import numpy as np
import random
from depth.model.DepthEucl import DepthEucl

#
#-----------------------   Center Point Algorism ----------------------- #
#

def go_to_center_point(weight, self_position, other_agents_positions, F):
    # TODO: もっといいアルゴリズムに
    other_agents_positions = np.array(other_agents_positions)

    model=DepthEucl().load_dataset(other_agents_positions)
    depths = model.halfspace(other_agents_positions, exact=True)

    center_idx = depths.argmax()
    centerpoint = other_agents_positions[center_idx]

    return weight * self_position + (1 - weight) * centerpoint.copy()

#
#-----------------------   Turley's Hyperplane Algorism ----------------------- #
#

def update_by_turkey_hyperplane(self_position, other_agents_positions, cur_time, F, dimension, find_best, diminish_step_length = False):
    if find_best:
        nomal_vector = best_nomal_of_hyperplane(
            self_position = self_position,
            other_agents_positions = other_agents_positions,
            F = F,
            dimension = dimension
        )
    else :
        nomal_vector = first_found_normal_of_hyperplane(
            self_position = self_position,
            other_agents_positions = other_agents_positions,
            F = F,
            dimension = dimension
        )
    step_length = 10 * (0.9 ** cur_time) if diminish_step_length else 10
    
    return self_position.copy() + nomal_vector * step_length


# 条件を満たす hyperplane の法線ベクトルのうち、最初に見つかったものを返す. ただし法線ベクトルは単位ベクトルとする.
def first_found_normal_of_hyperplane(self_position, other_agents_positions, F, dimension):
    for counter in range(100):
        # hyperplane の単位法線ベクトル (nomal_vector) をランダムに生成
        nomal_vector = get_random_unit_vector(dimension)
        side_count_diff = calc_signed_side_count_difference(nomal_vector, self_position, other_agents_positions)
        
        if side_count_diff > F:
            return nomal_vector
        elif (-1) * side_count_diff >  F:
            return (-1) * nomal_vector
            
    print("Not found good hyperplane")
    return np.zeros(dimension)

# 条件を満たす hyperplane の法線ベクトルのうち、その hyperplane が最も不均衡に Agents を分割するものを返す. ただし法線ベクトルは単位ベクトルとする.
def best_nomal_of_hyperplane(self_position, other_agents_positions, F, dimension):
    best_nomal_vector_set = {'nomal_vector': None, 'side_count_diff': 0}

    for counter in range(100):
        # hyperplane の単位法線ベクトル (nomal_vector) をランダムに生成
        nomal_vector = get_random_unit_vector(dimension)
        side_count_diff = calc_signed_side_count_difference(nomal_vector, self_position, other_agents_positions)

        if side_count_diff > F:
            if side_count_diff > best_nomal_vector_set['side_count_diff']:
                best_nomal_vector_set['nomal_vector'] = nomal_vector                    
                best_nomal_vector_set['side_count_diff'] = side_count_diff
        elif (-1) * side_count_diff > F:
            if (-1) * side_count_diff > best_nomal_vector_set['side_count_diff']:
                best_nomal_vector_set['nomal_vector'] = (-1) * nomal_vector                    
                best_nomal_vector_set['side_count_diff'] = (-1) * side_count_diff
    
    if best_nomal_vector_set['nomal_vector'] is None:
        print("Not found good hyperplane")
        return np.zeros(dimension)

    else:   
        return best_nomal_vector_set['nomal_vector']


def get_random_unit_vector(dimension):
    rng = np.random.default_rng()
    v = rng.standard_normal(dimension)
    norm = np.linalg.norm(v)
    nomal_vector = v / norm
    return nomal_vector


# 法線ベクトル normal_vector と self_position で定義される超平面について、正側の agent 数と負側の agent 数の差分を返す。
# 返り値は符号付きで、正なら正側優勢、負なら負側優勢。
def calc_signed_side_count_difference(nomal_vector, self_position, other_agents_positions):
    nodes_on_positive_side = 0  # hyperplane の nomal_vector 側にある agent の数
    nodes_on_negative_side = 0  # hyperplane の nomal_vector と逆側にある agent の数
    for other_position in other_agents_positions:
        inner_product = nomal_vector @ (other_position - self_position)
        if inner_product > 0:
            nodes_on_positive_side += 1
        elif inner_product < 0:
            nodes_on_negative_side += 1
    side_count_diff = nodes_on_positive_side - nodes_on_negative_side
    return side_count_diff