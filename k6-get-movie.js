import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 100, // 10 virtual users
  duration: '1m', // selama 1 menit
};

export default function () {
  let res = http.get('http://192.168.11.12:8000/v1/movie');
  check(res, {
    'status was 200': (r) => r.status === 200,
  });
} 