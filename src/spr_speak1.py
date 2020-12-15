#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gcp_texttospeech.srv import TTS
#音声認識
from voice_common_pkg.srv import SpeechToText

import rospy
import Levenshtein as lev

from spr_speak.srv import SprInformation
from spr_speak.srv import SprInformationResponse

file='/home/nao/catkin_ws/src/spr_speak/question_answer' #作成場所の指定

class RecognitionAnswer():
    def __init__(self):
        self.question_list=[]
        self.answer_list=[]

        with open(file,'r') as f:
            for str in f:
                if "q:" in str:
                    self.question_list.append(str.replace('q:', ''))
                else:
                    print str.replace('a:', '')
                    self.answer_list.append(str.replace('a:', ''))
        print('server is ready')
        rospy.wait_for_service('/tts')
        rospy.wait_for_service('/stt_server')

        self.stt_srv=rospy.ServiceProxy('/stt_server',SpeechToText)
        rospy.Service('/spr_speak',SprInformation,self.main)
        self.tts_srv=rospy.ServiceProxy('/tts', TTS)
        rospy.spin()

    def select_question(self):
        decision_number=0.6
        decision_sub=0.0
        question = -1

        while(question==-1):
            string=self.stt_srv(short_str=False)
            for i in range(len(self.question_list)):
                decision_sub=lev.distance(string.result_str, self.question_list[i])/(max(len(string.result_str), len(self.question_list[i])) *1.00)
                if decision_sub<decision_number:
                    decision_number=decision_sub
                    question=i
            if question==-1:
                self.tts_srv('please one more time')



        return question

    def answer_make(self,str,question):
        lavel_ls=[]
        value_ls=[]
        #ラベルと値を分けて添字で紐付けできるように
        for cnt,info in enumerate(str.split()):
            if cnt%2==0:
                lavel_ls.append('{'+info+'}')
            else:
                value_ls.append(info)

        #ラベル検索・値の置き換え
        for cnt,lavel in enumerate(lavel_ls):
            if lavel in self.answer_list[question]:
                str=self.answer_list[question].replace(lavel,value_ls[cnt])
                self.answer_list[question]=str



    def main(self,req):
        answer_num = self.select_question()
        self.answer_make(req.some_info,answer_num)

        return SprInformationResponse(self.answer_list[answer_num])





if __name__=='__main__':
    rospy.init_node('spr_speak')
    i=RecognitionAnswer()
    i.main()
