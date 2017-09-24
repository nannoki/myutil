
import sys
from pathlib import Path
import mojimoji
import MeCab

class TextProc:
    def __init__(self):
        self.tagger = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
        # tagger = MeCab.Tagger('-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
        # tagger = MeCab.Tagger('mecabrc')

        # おまじない。既知のバグ回避らしい。
        self.tagger.parse('')

        # 使用する品詞。全部使うときは target = None
        # '名詞', '動詞', '形容詞'
        # self.targets = None
        self.targets = ['名詞', '動詞', '形容詞']
        # レベル２の例外（例えば、数字は　名詞＞数字）
        self.target_except = ['数', '固有名詞']

        # '表層': 0, '読み': 1, '原形': 2
        self.word_type = 2

        # 全角半角変換： しない=0, 全角から半角へ=1, 半角から全角へ=2
        self.zenhan_type = 1
        # 変換オプション(kana: かな・カナ, digit: 数字, ascii: 記号)
        self.zenhan_option = {'kana': False, 'digit': True, 'ascii': True}


    def trans_zenhan(self, sentence, zenhan_type=None, zenhan_option=None):
        """
        全角、半角変換
        """
        if zenhan_type is None:
            zenhan_type = self.zenhan_type
        if zenhan_option is None:
            zenhan_option = self.zenhan_option

        if zenhan_type == 0:
            return sentence
        elif zenhan_type == 1:
            return mojimoji.zen_to_han(sentence, **zenhan_option)
        elif zenhan_type == 2:
            return mojimoji.han_to_zen(sentence, **zenhan_option)
        else:
            exit(True)


    def select_token(self, sentence, targets=None):
        """
        品詞選択し、分かち書き
        """
        if targets is None:
            targets = self.targets
        result = []
        node = self.tagger.parseToNode(sentence)
        while node:
            feats = node.feature.split(',')
            # todo targetsに「助動詞」があると「動詞」もヒットするけど、そういう指定は通常しないのでとりあえず放置
            if ((self.targets is None) or (feats[0] in targets)) and (feats[1] not in self.target_except):
                # 表層（入力文字列そのまま）
                if self.word_type == 0:
                    result.append(node.surface)
                # 読み
                elif self.word_type == 1:
                    result.append(feats[-1])
                # 原形
                elif self.word_type == 2:
                    result.append(feats[-3] if feats[-3] != '*' else node.surface)
                else:
                    print('word_typeが想定外')
                    exit(True)

            node = node.next

        # for word in sentence:
        #     if (targets is None) or (word[3].split('-')[0] in targets):
        #
        #         result.append(word[word_type])
        return ' '.join(result)


    def all_proc(self, input_file, output_file):
        """
        文章全体をまとめて投入すると、改行が消えてしまうので、1行単位で実行。
        他のやり方あるかもれないけど。
        """
        p = Path(output_file)
        if p.exists():
            print('出力先ファイルがすでに存在します。')
            print('上書き（既存ファイルは削除）する場合は "over write"、 追記する場合は "append" と入力してください。')
            while True:
                user_input = input('[over write | append] > ')
                if user_input == 'over write':
                    print('上書きします。')
                    p.unlink()
                    break
                elif user_input == 'append':
                    print('追記します。')
                    break
                else:
                    print('入力が正しくありません :', user_input)

        with open(input_file, 'r') as fi:
            with open(output_file, 'a') as fo:
                for sentence in fi:
                    # 全角半角変換。形態素解析には影響ないみたい。
                    sentence = self.trans_zenhan(sentence)
                    parsed_sentence = self.select_token(sentence)
                    parsed_sentence = parsed_sentence.lower()
                    fo.writelines(parsed_sentence + '\n')

                
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print('引数が不正です。\n'
              '第1引数（必須） : 入力ファイルの固定の絶対パス\n'
              '第2引数(任意) : 出力ファイルの絶対パス')
    else:
        print('arg1 - input file  :', args[1])
        print('arg2 - output file :', args[2])
        textproc = TextProc()
        textproc.all_proc(args[1], args[2])


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
