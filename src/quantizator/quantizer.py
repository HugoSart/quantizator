from abc import abstractmethod

import numpy as np

import quantizator.util as util


class Quantizer:
    """
    Classe abstrata que representa um algorítmo de quantização de cores de uma imagem.
    A imagem a ser quantizada é mesma passada como parâmetro no construtor de um objeto que herda esta classe.
    """

    def __init__(self, img):
        self.img = img

    @abstractmethod
    def quantize(self, n):
        pass


class SimpleQuantizer(Quantizer):
    """
    Implementação do Quantizer utilizando um algorítmo de quantização simples.
    """

    def quantize(self, n):
        nums = util.nmult(n)
        print('Iniciando quantização uniforme com %d cores divididas em RGB(%d, %d, %d) ...' % (n, nums[0], nums[1], nums[2]))

        m = np.amax(self.img) + 1
        rgb = np.zeros(self.img.shape, 'uint8')
        for i in range(3):
            aux = np.uint8(self.img[..., i] * float(nums[i] / m))
            rgb[..., i] = np.uint8(127 if nums[i] == 1 else (aux / (nums[i] - 1.)) * 255)

        return rgb


class MedianCutQuantizer(Quantizer):
    """
    Implementação do Quantizer utilizando um algorítmo de quantização que usa mediancut.
    """

    def quantize(self, n):
        bucket = []
        palheta = []
        dispersao = []
        # pega rgb de todos pixels e coloca em um array ordenado
        # esse array é jogado em um bucket

        colors = np.concatenate(self.img[:, :], axis=0)
        colors = np.unique(colors, axis=0)

        # descobre qual cor tem a maior dispersão e ordena
        for i in range(3):
            dispersao.append(np.amax(colors[:, i]) - np.amin(colors[:, i]))
        dispersao_key = dispersao.index(max(dispersao))
        colors = sorted(colors, key=lambda x: x[dispersao_key])

        bucket.append(colors)
        print(colors)
        print('bucket', bucket)

        # divide o bucket original em n buckets em que n = numero de cores
        while len(bucket) <= n:
            tamanho = len(bucket)
            new_bucket = []
            for i in range(tamanho):
                meio = int(len(bucket[i]) / 2)
                a = bucket[i][:meio]
                b = bucket[i][meio:]
                print('a', a)
                new_bucket.append(a)
                new_bucket.append(b)
            bucket = new_bucket

        # Palheta pelo pixel do meio
        # identifica a cor mediana para cada um dos buckets de cor
        for i in range(len(bucket)):
            meio = int(len(bucket[i]) / 2)
            palheta.append(bucket[i][meio])

        # Palheta por média dos pixels (ta meio bugado)
        # palheta2 = []
        # for i in range(len(bucket)):
        #     npbucket = np.array(bucket[i])
        #     palheta2.append(np.array([np.mean(npbucket[:, 0]), np.mean(npbucket[:, 1]), np.mean(npbucket[:, 2])], dtype='uint8'))

        palheta = np.array(palheta).reshape(-1, 3)
        # para cada pixel da imagem, faz a distância entre esse pixel e cada um dos elementos da palheta de cores
        # armazena a distância como um elemento do vetor distance
        distancia = np.linalg.norm(self.img[:, :, None] - palheta[None, None, :], axis=3)
        # pega o índice de qual a cor de menor distância
        indices_palheta = np.argmin(distancia, axis=2)
        # cria a imagem nova com base na palheta
        img = palheta[indices_palheta]

        return img
