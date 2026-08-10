import importlib.util, io, os, unittest
from pathlib import Path
ROOT=Path(__file__).parent
os.environ.update({
 'RCC_DEMO_MODE':'1',
 'RCC_EXPECTED_HOST':'example.invalid',
 'RCC_TRUSTED_PROXY_CIDRS':'127.0.0.0/8,::1/128',
 'RCC_REQUIRED_GROUP':'project_demo',
 'RCC_DATABASE':str(ROOT/'demo.sqlite3'),
})
exec(compile((ROOT/'init_demo_data.py').read_text(), str(ROOT/'init_demo_data.py'), 'exec'))
spec=importlib.util.spec_from_file_location('example_app', ROOT/'app.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)

def call(path='/', addr='127.0.0.1', user='alice', groups='project_demo', method='GET'):
    status=[]; headers=[]
    def start(s,h): status.append(s); headers.extend(h)
    env={'PATH_INFO':path,'REQUEST_METHOD':method,'REMOTE_ADDR':addr,'HTTP_HOST':'example.invalid','HTTP_REMOTE_USER':user,'HTTP_REMOTE_GROUPS':groups,'wsgi.input':io.BytesIO()}
    body=b''.join(app.application(env,start))
    return status[0], dict(headers), body

class ProtectedAppTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        (ROOT/'demo.sqlite3').unlink(missing_ok=True)
    def test_authorized_user(self): self.assertTrue(call()[0].startswith('200'))
    def test_direct_client_denied(self): self.assertTrue(call(addr='192.0.2.10')[0].startswith('403'))
    def test_wrong_group_denied(self): self.assertTrue(call(groups='project_other')[0].startswith('403'))
    def test_post_denied(self): self.assertTrue(call(method='POST')[0].startswith('405'))
    def test_arbitrary_path_not_exposed(self): self.assertTrue(call('/files/../../etc/passwd')[0].startswith('404'))
    def test_curated_file(self):
        status,_,body=call('/files/0123456789abcdef0123456789abcdef')
        self.assertTrue(status.startswith('200')); self.assertEqual(body,b'RCC_PROTECTED_FILE_OK\n')

if __name__=='__main__': unittest.main()
