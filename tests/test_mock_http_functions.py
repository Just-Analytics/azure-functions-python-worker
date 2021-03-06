from azure.worker import protos
from azure.worker import testutils


class TestMockHost(testutils.AsyncTestCase):

    async def test_call_sync_function_check_logs(self):
        async with testutils.start_mockhost() as host:
            await host.load_function('sync_logging')

            invoke_id, r = await host.invoke_function(
                'sync_logging', [
                    protos.ParameterBinding(
                        name='req',
                        data=protos.TypedData(
                            http=protos.RpcHttp(
                                method='GET')))
                ])

            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)

            self.assertEqual(len(r.logs), 1)

            log = r.logs[0]
            self.assertEqual(log.invocation_id, invoke_id)
            self.assertEqual(log.message, 'a gracefully handled error')

            self.assertEqual(r.response.return_value.string, 'OK-sync')

    async def test_call_async_function_check_logs(self):
        async with testutils.start_mockhost() as host:
            await host.load_function('async_logging')

            invoke_id, r = await host.invoke_function(
                'async_logging', [
                    protos.ParameterBinding(
                        name='req',
                        data=protos.TypedData(
                            http=protos.RpcHttp(
                                method='GET')))
                ])

            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)

            self.assertEqual(len(r.logs), 2)

            self.assertEqual(r.logs[0].invocation_id, invoke_id)
            self.assertEqual(r.logs[0].message, 'one error')

            self.assertEqual(r.logs[1].invocation_id, invoke_id)
            self.assertEqual(r.logs[1].message, 'and another error')

            self.assertEqual(r.response.return_value.string, 'OK-async')

    async def test_handles_unsupported_messages_gracefully(self):
        async with testutils.start_mockhost() as host:
            # Intentionally send a message to worker that isn't
            # going to be ever supported by it.  The idea is that
            # workers should survive such messages and continue
            # their operation.  If anything, the host can always
            # terminate the worker.
            await host.send(
                protos.StreamingMessage(
                    worker_heartbeat=protos.WorkerHeartbeat()))

            _, r = await host.load_function('return_out')
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Success)

            for log in r.logs:
                if 'unknown StreamingMessage' in log.message:
                    break
            else:
                raise AssertionError('the worker did not log about an '
                                     '"unknown StreamingMessage"')
