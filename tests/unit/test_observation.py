import datetime
import unittest

import datapoint


class ObservationTestCase(unittest.TestCase):

    def setUp(self):
        self.observation = datapoint.Observation.Observation()

    def test_observation(self):
        # Just copy the forecast test
        test_day = datapoint.Day.Day()
        test_day.date = datetime.datetime.utcnow()

        test_timestep = datapoint.Timestep.Timestep()
        test_timestep.name = 1

        test_day.timesteps.append(test_timestep)

        self.observation.days.append(test_day)

        # What is this asserting?
        assert self.observation.now()
