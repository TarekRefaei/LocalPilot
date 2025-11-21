export const VIEW_CONTAINER_ID = 'localpilot';

export const VIEW_IDS = {
  chat: 'localpilot.views.chat',
  plans: 'localpilot.views.plans',
  act: 'localpilot.views.act',
  indexing: 'localpilot.views.indexing',
  status: 'localpilot.views.status',
} as const;

export const COMMAND_IDS = {
  helloWorld: 'localpilot.helloWorld',
  showViews: 'localpilot.showViews',
  focusChatInput: 'localpilot.focusChatInput',
  chatTransferToPlan: 'localpilot.chat.transferToPlan',
  planCreate: 'localpilot.plan.create',
  planUpdate: 'localpilot.plan.update',
  planDelete: 'localpilot.plan.delete',
  actDryRun: 'localpilot.act.dryRun',
  actApprove: 'localpilot.act.approve',
  actApply: 'localpilot.act.apply',
  actRollback: 'localpilot.act.rollback',
  indexStart: 'localpilot.index.start',
  indexStop: 'localpilot.index.stop',
  modelSwap: 'localpilot.model.swap',
} as const;

export type ViewId = (typeof VIEW_IDS)[keyof typeof VIEW_IDS];
export type CommandId = (typeof COMMAND_IDS)[keyof typeof COMMAND_IDS];
