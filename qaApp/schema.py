import re
from .models import IndivdualQuestion, IndividualTopic, StudentQuestion, StudentTopic
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


class IndividualTopics(DjangoObjectType):
    class Meta:
        model = IndividualTopic
        fields = ('id', 'title')


class IndividualQuestions(DjangoObjectType):
    class Meta:
        model = IndivdualQuestion
        fields = ('topic', 'question', 'answer')


class StudentTopics(DjangoObjectType):
    class Meta:
        model = StudentTopic
        fields = ('id', 'course_code', 'course_title')


class StudentTopicInput(graphene.InputObjectType):
    course_code = graphene.String()
    course_title = graphene.String()


class StudentQuestions(DjangoObjectType):
    class Meta:
        model = StudentQuestion
        fields = ('course_code', 'question', 'answer')


class IndividualTopicNode(DjangoObjectType):
    class Meta:
        model = IndividualTopic
        filter_fields = {
            'title': ['icontains'],
        }
        interfaces = (relay.Node, )


class StudentTopicNode(DjangoObjectType):
    class Meta:
        model = StudentTopic
        filter_fields = {
            'course_code': ['icontains'],
            'course_title': ['icontains']
        }
        interfaces = (relay.Node, )


class IndividualQuestionNode(DjangoObjectType):
    class Meta:
        model = IndivdualQuestion
        filter_fields = {
            'question': ['icontains'],
        }
        interfaces = (relay.Node, )


class StudentQuestionNode(DjangoObjectType):
    class Meta:
        model = StudentQuestion
        filter_fields = {
            'question': ['icontains'],
        }
        interfaces = (relay.Node, )


class CreateIndividualTopic(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    topic = graphene.Field(IndividualTopics)

    @classmethod
    def mutate(cls, root, info, title):
        topic = IndividualTopic(title=title, owner=info.context.user)
        topic.save()
        return CreateIndividualTopic(topic=topic)


class CreateStudentTopic(graphene.Mutation):
    class Arguments:
        course_code = graphene.String(required=True)
        course_title = graphene.String(required=True)
    course = graphene.Field(StudentTopics)

    @classmethod
    def mutate(cls, root, info, course_code, course_title):
        course = StudentTopic(course_code=course_code,
                              course_title=course_title, owner=info.context.user)
        course.save()
        return CreateStudentTopic(course=course)


class CreateIndividualQuestion(graphene.Mutation):
    class Arguments:
        topic = graphene.ID(required=True)
        question = graphene.String(required=True)
        answer = graphene.String()
    topicQuestion = graphene.Field(IndividualQuestions)

    @classmethod
    def mutate(cls, root, info, topic, question, answer):
        topicInstance = IndividualTopic.objects.get(id=topic)
        topicQuestion = IndivdualQuestion(topic=topicInstance, question=question,
                                          answer=answer, owner=info.context.user)
        topicQuestion.save()
        return CreateIndividualQuestion(topicQuestion=topicQuestion)


class CreateStudentQuestion(graphene.Mutation):
    class Arguments:
        course_code = graphene.ID(required=True)
        question = graphene.String(required=True)
        answer = graphene.String()
    courseQuestion = graphene.Field(StudentQuestions)

    @classmethod
    def mutate(cls, root, info, course_code, question, answer):
        course_code_instance = StudentTopic.objects.get(
            id=course_code)
        courseQuestion = StudentQuestion(course_code=course_code_instance, question=question,
                                         answer=answer, owner=info.context.user)
        courseQuestion.save()
        return CreateStudentQuestion(courseQuestion=courseQuestion)


class MutateIndividualTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
    topic = graphene.Field(IndividualTopics)

    @classmethod
    def mutate(cls, root, info, title, id):
        topic = IndividualTopic.objects.get(id=id)
        topic.title = title
        topic.owner = info.context.user
        topic.save()
        return MutateIndividualTopic(topic=topic)


class MutateStudentTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = StudentTopicInput()
    course = graphene.Field(StudentTopics)

    @classmethod
    def mutate(cls, root, info, id, input):
        course = StudentTopic.objects.get(id=id)
        if input.course_code:
            course.course_code = input.course_code
        if input.course_title:
            course.course_title = input.course_title
        course.owner = info.context.user
        course.save()
        return MutateStudentTopic(course=course)


class ModelMutation(graphene.ObjectType):
    create_individual_topic = CreateIndividualTopic.Field()
    update_individual_topic = MutateIndividualTopic.Field()
    create_student_topic = CreateStudentTopic.Field()
    update_student_topic = MutateStudentTopic.Field()
    create_student_question = CreateStudentQuestion.Field()
    create_individual_question = CreateIndividualQuestion.Field()


class ModelQuery(graphene.ObjectType):

    individual_topics = graphene.List(IndividualTopics)

    individual_questions = graphene.List(
        IndividualQuestions, topic_id=graphene.ID())

    student_questions = graphene.List(
        StudentQuestions, course_code_id=graphene.ID())
    student_topics = graphene.List(StudentTopics)

    #individual_topic_search = relay.Node.Field(IndividualTopicNode)
    all_individual_topic_search = DjangoFilterConnectionField(
        IndividualTopicNode)
    #student_topic_search = relay.Node.Field(StudentTopicNode)
    all_student_topic_search = DjangoFilterConnectionField(
        StudentTopicNode)
    all_individual_question_search = DjangoFilterConnectionField(
        IndividualQuestionNode)
    all_student_question_search = DjangoFilterConnectionField(
        StudentQuestionNode)

    def resolve_individual_topics(root, info):
        return IndividualTopic.objects.all()

    def resolve_individual_questions(root, info, topic_id):
        return IndivdualQuestion.objects.filter(topic=topic_id)

    def resolve_student_topics(root, info):
        return StudentTopic.objects.all()

    def resolve_student_questions(root, info, course_code_id):
        return StudentQuestion.objects.filter(course_code=course_code_id)


# It remain doing all those icontains for topics then searchin for questions relating to it.
