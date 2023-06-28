# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

pytest_rally = pytest.importorskip("pytest_rally")


class TestTrackRepository:
    skip_tracks = ["elastic/logs", "elastic/security", "sql", "serverless_k8s"]
    disable_assertions = {"http_logs": ["append-no-conflicts", "runtime-fields"], "nyc_taxis": ["update-aggs-only"]}
    skip_challenges = ["esql"]

    def test_autogenerated(self, es_cluster, rally, track, challenge, rally_options):
        track_params = {}
        if track not in self.skip_tracks and challenge not in self.skip_challenges:
            if challenge in self.disable_assertions.get(track, []):
                rally_options.update({"enable_assertions": False})
            if challenge == "runtime-fields":
                track_params = {"runtime_fields": "true"}
            ret = rally.race(track=track, challenge=challenge, track_params=track_params, **rally_options)
            assert ret == 0
        else:
            pytest.skip(msg=f"{track}-{challenge} included in skip list")
