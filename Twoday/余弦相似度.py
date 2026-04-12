import numpy as np

def cos_mul(vec1,vec2):
    if(len(vec1)!=len(vec2)):
        raise ValueError("向量长度不一致")
    sum = 0
    for a,b in zip(vec1,vec2):
        sum += a*b
    return sum

def cos_norm(vec):
    sum = 0
    for a in vec:
        sum += a*a
    # 开方
    return np.sqrt(sum)

def cos_similarity(vec1,vec2):
    return cos_mul(vec1,vec2)/(cos_norm(vec1)*cos_norm(vec2))

if __name__ == "__main__":
    vec1 = [1,2,3]
    vec2 = [4,5,6]
    print(cos_similarity(vec1,vec2))