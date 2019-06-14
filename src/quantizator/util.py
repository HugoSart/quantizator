import numpy as np


def nmult(n):
    """
    Separa um número em três números onde a multiplicação destes três números resulta no número original.

    :param n: o número a ser fatorado em três números.
    :return: um array de três posições com os números fatorados.
    """
    # Verificação de segurança para n menor do que 1
    if n <= 1:
        return [1, 1, 1]

    c = n
    nums = []

    # Fatora o número n de forma convensional
    for i in range(2, n + 1):
        while c % i == 0:
            nums.append(i)
            c /= i

    if len(nums) == 1:
        nums = [nums[0], 1, 1]
    elif len(nums) == 2:
        nums = [nums[0], nums[1], 1]
    elif len(nums) > 3:
        # Se o número de elementos da fatoração for maior do que três, comprime o array em um de três posições fazendo
        # a multiplicação do último elemento do array com o menor elemento do array desconsiderando a si mesmo
        while len(nums) > 3:
            i1 = np.argmin(nums)
            n1 = nums[i1]
            nums.pop(i1)
            i2 = np.argmin(nums)
            nums[i2] *= n1

    return nums


def aprox(img, palheta):
    palheta = np.array(palheta).reshape(-1, 3)
    distancia = np.linalg.norm(img[:, :, None] - palheta[None, None, :], axis=3)
    indices_palheta = np.argmin(distancia, axis=2)
    return palheta[indices_palheta]


def argmedian(array, column):
    return np.argsort(array[:, column])[len(array) // 2]


def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.math.log10(PIXEL_MAX / np.math.sqrt(mse))

