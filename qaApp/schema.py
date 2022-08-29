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


class StudentQuestions(DjangoObjectType):
    class Meta:
        model = StudentQuestion
        fields = ('course_code', 'question', 'answer')


class CreateIndividualTopic(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    topic = graphene.Field(IndividualTopics)

    @classmethod
    def mutate(cls, root, info, title):
        topic = IndividualTopic(title=topic, owner=info.context.user)
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
        topic = graphene.Int(required=True)
        question = graphene.String(required=True)
        answer = graphene.String()
    topicQuestion = graphene.Field(IndividualQuestions)

    @classmethod
    def mutate(cls, root, info, topic, question, answer):
        topicQuestion = IndividualQuestions(topic=topic, question=question,
                                            answer=answer, owner=info.context.user)
        topicQuestion.save()
        return CreateIndividualQuestion(topicQuestion=topicQuestion)


class CreateStudentQuestion(graphene.Mutation):
    class Arguments:
        course_code = graphene.Int(required=True)
        question = graphene.String(required=True)
        answer = graphene.String()
    topicQuestion = graphene.Field(StudentQuestions)

    @classmethod
    def mutate(cls, root, info, course_code, question, answer):
        topicQuestion = StudentQuestions(course_code=course_code, question=question,
                                         answer=answer, owner=info.context.user)
        topicQuestion.save()
        return CreateStudentQuestion(topicQuestion=topicQuestion)


class MutateIndividualTopic(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
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
        id = graphene.Int(required=True)
        course_code = graphene.String()
        course_title = graphene.String()
    course = graphene.Field(StudentTopics)

    @classmethod
    def mutate(cls, root, info, course_title, id, course_code):
        course = IndividualTopic.objects.get(id=id)
        course.course_code = course_code
        course.course_title = course_title
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
        IndividualQuestions, topic_id=graphene.Int())

    student_questions = graphene.List(
        StudentQuestions, course_code_id=graphene.Int())
    student_topics = graphene.List(StudentTopics)

    def resolve_individual_topics(root, info):
        return IndividualTopic.objects.all()

    def resolve_individual_questions(root, info, topic_id):
        return IndivdualQuestion.objects.filter(topic=topic_id)

    def resolve_student_topics(root, info):
        return StudentTopic.objects.all()

    def resolve_student_questions(root, info, course_code_id):
        return StudentQuestion.objects.filter(course_code=course_code_id)


# It remain doing all those icontains for topics then searchin for questions relating to it.
