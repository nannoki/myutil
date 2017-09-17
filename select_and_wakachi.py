

import mojimoji
import MeCab
tagger = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
# tagger = MeCab.Tagger('-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
# tagger = MeCab.Tagger('mecabrc')


# 使用する品詞。全部使うときは target = None
# '名詞', '動詞', '形容詞'
# targets = None
targets = ['名詞', '動詞', '形容詞']

# '表層': 0, '読み': 1, '原形': 2
word_type = 0

# 全角半角変換： しない=0, 全角から半角へ=1, 半角から全角へ=2
zenhan_type = 1
# 変換オプション(kana: かな・カナ, digit: 数字, ascii: 記号)
zenhan_option = {'kana': False, 'digit': True, 'ascii': True}


input_file = './data/alltext.txt'
output_file = './data/wakachi.txt'


def trans_zenhan(sentence):
    """
    全角、半角変換
    """
    if zenhan_type == 0:
        return sentence
    elif zenhan_type == 1:
        return mojimoji.zen_to_han(sentence, **zenhan_option)
    elif zenhan_type == 2:
        return mojimoji.han_to_zen(sentence, **zenhan_option)
    else:
        print('zenhan_typeが想定外')
        exit(True)


def select_token(sentence):
    """
    品詞選択し、分かち書き
    """
    result = []
    for word in sentence:
        if (targets is None) or (word[3].split('-')[0] in targets):
            # ここで小文字化。形態素解析前にやると、大文字混じりで出力されてしまう。
            # それで統一されるならいいけど、一応。
            # result.append(word[word_type].lower())
            result.append(word[word_type])
    return ' '.join(result)


if __name__ == '__main__':
    with open(input_file, 'r') as fi:
        with open(output_file, 'a') as fo:
            for sentence in fi:
                # 全角半角変換。形態素解析には影響ないみたい。
                sentence = trans_zenhan(sentence)
                parsed_sentence = tagger.parse(sentence).split('\n')
                parsed_sentence = [word.split('\t') for word in parsed_sentence if (len(word) > 0) and (word != 'EOS')]
                parsed_sentence = select_token(parsed_sentence)
                parsed_sentence = parsed_sentence.lower()
                fo.writelines(parsed_sentence + '\n')


"""
参考
全部じゃないかも

連体詞
名詞-副詞可能
名詞-非自立-副詞可能
名詞-非自立-助動詞語幹
名詞-非自立-形容動詞語幹
名詞-非自立-一般
名詞-特殊-助動詞語幹
名詞-代名詞-一般
名詞-接尾-副詞可能
名詞-接尾-特殊
名詞-接尾-地域
名詞-接尾-人名
名詞-接尾-助動詞語幹
名詞-接尾-助数詞
名詞-接尾-形容動詞語幹
名詞-接尾-一般
名詞-接尾-サ変接続
名詞-接続詞的
名詞-数
名詞-固有名詞-地域-国
名詞-固有名詞-地域-一般
名詞-固有名詞-組織
名詞-固有名詞-組織
名詞-固有名詞-人名-名
名詞-固有名詞-人名-姓
名詞-固有名詞-人名-一般
名詞-固有名詞-一般
名詞-形容動詞語幹
名詞-一般
名詞-ナイ形容詞語幹
名詞-サ変接続
副詞-助詞類接続
副詞-一般
動詞-非自立
動詞-接尾
動詞-自立
接頭詞-名詞接続
接頭詞-動詞接続
接頭詞-数接続
接続詞
助動詞
助詞-連体化
助詞-並立助詞
助詞-副助詞／並立助詞／終助詞
助詞-副助詞
助詞-副詞化
助詞-特殊
助詞-接続助詞
助詞-終助詞
助詞-係助詞
助詞-格助詞-連語
助詞-格助詞-引用
助詞-格助詞-一般
形容詞-非自立
形容詞-接尾
形容詞-自立
記号-読点
記号-句点
記号-括弧閉
記号-括弧開
記号-一般
記号-アルファベット
感動詞

"""
