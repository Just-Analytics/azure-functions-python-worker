from azure.worker import protos
from azure.worker import testutils


class TestMockHost(testutils.AsyncTestCase):

    async def test_load_broken__missing_py_param(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('missing_py_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r".*cannot load the missing_py_param function"
                r".*parameters are declared in function.json"
                r".*'req'.*")

    async def test_load_broken__missing_json_param(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('missing_json_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r".*cannot load the missing_json_param function"
                r".*parameters are declared in Python"
                r".*'spam'.*")

    async def test_load_broken__wrong_param_dir(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('wrong_param_dir')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the wrong_param_dir function'
                r'.*binding foo is declared to have the "out".*')

    async def test_load_broken__wrong_binding_dir(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('wrong_binding_dir')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the wrong_binding_dir function'
                r'.* binding foo is declared to have the "in" direction'
                r'.*but its annotation is.*Out.*')

    async def test_load_broken__invalid_context_param(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_context_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_context_param function'
                r'.*the "context" parameter.*')

    async def test_load_broken__syntax_error(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('syntax_error')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertIn('SyntaxError', r.response.result.exception.message)

    async def test_load_broken__inout_param(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('inout_param')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the inout_param function'
                r'.*"inout" bindings.*')

    async def test_load_broken__return_param_in(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('return_param_in')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the return_param_in function'
                r'.*"\$return" .* set to "out"')

    async def test_load_broken__invalid_return_anno(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_return_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_return_anno function'
                r'.*Python return annotation "str" does not match '
                r'binding type "http"')

    async def test_load_broken__invalid_return_anno_non_type(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function(
                'invalid_return_anno_non_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_return_anno_non_type function: '
                r'has invalid non-type return annotation 123')

    async def test_load_broken__invalid_http_trigger_anno(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_http_trigger_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_http_trigger_anno function'
                r'.*type of req binding .* "httpTrigger" '
                r'does not match its Python annotation "int"')

    async def test_load_broken__invalid_out_anno(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_out_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_out_anno function'
                r'.*type of ret binding .* "bytes" '
                r'does not match its Python annotation "float"')

    async def test_load_broken__invalid_in_anno(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_in_anno')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_in_anno function'
                r'.*type of req binding .* "httpTrigger" '
                r'does not match its Python annotation "HttpResponse"')

    async def test_load_broken__invalid_in_anno_non_type(self):
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('invalid_in_anno_non_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the invalid_in_anno_non_type function: '
                r'binding req has invalid non-type annotation 123')

    async def test_load_broken__unsupported_bind_type(self):
        # Test that we won't load a function with a bind type we don't support.
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('unsupported_bind_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the unsupported_bind_type function'
                r'.*unknown type .* "yolo".*')

    async def test_load_broken__unsupported_ret_type(self):
        # Test that we won't load a function with a bind type we don't support.
        async with testutils.start_mockhost(
                script_root='broken_functions') as host:

            func_id, r = await host.load_function('unsupported_ret_type')

            self.assertEqual(r.response.function_id, func_id)
            self.assertEqual(r.response.result.status,
                             protos.StatusResult.Failure)

            self.assertRegex(
                r.response.result.exception.message,
                r'.*cannot load the unsupported_ret_type function'
                r'.*unknown type .*\$return.* "yolo".*')
