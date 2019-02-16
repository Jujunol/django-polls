import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(text="", **kwargs):
    """
    Creates a Question with the provided text with pub_date set to 
    the amount of time using kwargs into the future. Use negative for past.
    """
    time = timezone.now() + datetime.timedelta(**kwargs)
    return Question.objects.create(text=text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in the future
        """
        future_question = create_question(days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is a day old
        """
        old_question = create_question(days=-1, seconds=-1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose
        pub_date is within the past day
        """
        recent_question = create_question(hours=-23, minutes=-59, seconds=-59)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on
        the index page
        """
        create_question(text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed
        on the index page
        """
        create_question(text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_question(self):
        """
        Even when both past and future questions exist, only past
        questions will be displayed
        """
        create_question(text="Past Question", days=-30)
        create_question(text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple
        """
        create_question(text="Past Question 1", days=-30)
        create_question(text="Past Question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question 2>', '<Question: Past Question 1>']
        )


class QuestionDetailsViewTests(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date
        in the future returns a 404 error
        """
        future_question = create_question(days=30)
        url = reverse('polls:details', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date
        in the past responds with the question's text
        """
        past_question = create_question(text="Past Question", days=-30)
        url = reverse('polls:details', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, "Past Question")


class QuestionResultsViewTest(TestCase):

    def test_future_question(self):
        """
        The result view of a question with a pub_date
        in the future returns a 404 error
        """
        future_question = create_question(days=30)
        url = reverse('polls:results', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The result view of a question with a pub_date
        in the past responds with the question's text
        """
        past_question = create_question(text="Past Question", days=-30)
        url = reverse('polls:results', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, "Past Question")


