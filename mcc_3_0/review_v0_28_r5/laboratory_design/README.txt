MCC 3.0 v0.28-r3 — Experimental falsification specification
Authors of book: Wonsik Choi and Jeongin Choi
Prepared: 2026-10-22. External publication not performed in this revision.

검증 입력
기준 본문은 v0.28-r2 한영 전체본. 122장의 동결 광학 모형 v1.0을 검토했다.
원전: DOI 10.5281/zenodo.23380920에 대응하는 보존 패키지의 optical_model_v1_0.
원전 파일 29개 해시 검증 뒤 reproduce.py를 실행하여 기존 17+11개 검사 통과.
NPZ 입력 SHA-256: 8c53fb73b332db2805b7d614f166511094b54b3f1b2a291fbfdfe46312408d6b.
계측 자료: NIST frequency-comb 및 uncertainty-methods 자료를 확인하여 본문 E1/E2에 명시.
외부 계측 자료는 WRRA를 실험적으로 검증한 자료가 아니다.

WRRA 고유 변환
128 SOURCE 평균응력 프로파일 → 고정 차등 위상 Hamiltonian → 유한 위상 합 → 가시도 곡선.
기존 변환과 입력을 그대로 사용한다. 이번 추가 기능은 그 곡선의 측정 설계와 공분산 검정이다.
새 숫자형 보정으로 결과를 맞추지 않았다. 광학 자연결합의 실현 절차는 미확정이다.

산출값
3파장(532/1064/1550 nm), 각 문턱/최소/회복 3점, 총 9점.
가시도 절대 표준불확도 목표 0.01. 이는 선택한 설계값이며 실측값이 아니다.
1064 nm 유효 노출 0–40 m. 최소 21.780958380 m, 회복 37.278764320 m.
일반 광로차 D=40 m와 1064 nm를 가정한 예시 잡음 목표:
주파수 RMS 53.371962 kHz, 광로차 RMS 7.576944 nm (위상 분산 반씩 배분).
유효 노출량 L과 장치 광로차 D는 다른 양이다.
독립 검출 시행 각 신호/기준 블록 98,766개는 이상적 계수통계 상계이며 실제 측정시간은 미정.
실행된 세부 수치와 검사 수는 design.json, test_results.json 참조.

반증조건
Gaussian 근사·알려진 공분산·사후 피팅 없음이면 Q>27.8771648713 (자유도9, alpha0.001)로 동결 분기 기각.
정상 합성 자료 Q=6.59879688770414, 종료0.
가시도 손실 없는 합성 자료 Q=7177.529448321479, 종료1.
회복 누락 합성 자료 Q=2105.0240834042634, 종료1.
해시변경·순서변경·비양정치 공분산 각각 종료2.
기각은 해당 준비와 결합이 실제 확인된 분기에 적용한다. 미확정 연결을 무시해 무신호를 반증으로 선언하지 않는다.
실험 비교에서 공분산 추정·모수 피팅을 추가하면 실제 검정분포를 별도로 교정해야 한다.

결론
한영 전체본 122.1절과 H.7에 측정 범위, 오차 예산, 대조군, 기각 규칙과 코드 실행 근거를 추가했다.
기존 v0.28-r2 N_U 보완을 보존했다. 실제 실험·전체 우주론 검증 완료를 주장하지 않는다.
정적 위상식에서는 셔터 간격이 소거되므로 콤으로 셔터 자체를 검출한다고 주장하지 않는다.
실험실 뒤틀림 응력 전달함수는 아직 계산하지 않았으며 임의의 실험 감도를 제시하지 않았다.

Reproduction (from package root):
python -m pip install numpy scipy matplotlib
python optical_model_v1_0/reproduce.py
python design.py
python test_design.py
python verify_observations.py synthetic_nominal.json
python verify_observations.py synthetic_no_loss.json
# Expected exit 1 for the last command is the intended rejection.
sh book_v0_28_r3/review/render.sh
# PDF build requires pandoc, xelatex and Noto Sans CJK KR.
# Original verify.py checks the pre-replay frozen source; replay can rewrite outputs.

Historical reports inside optical_model_v1_0 and inherited evidence keep their original dates and scopes.
Current results are recorded in optical_replay.log, source_hash_check.log, design.log and test_design.log.

Prior r2 scale_contract.py and finite_scale_original evidence are included unchanged for continuity; not rerun in this r3 turn. REVIEW_KO.txt describes that earlier revision.
