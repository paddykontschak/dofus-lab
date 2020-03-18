/** @jsx jsx */

import React from 'react';
import { jsx, css } from '@emotion/core';
import Card from 'antd/lib/card';
import Tooltip from 'antd/lib/tooltip';
import { useMutation, useApolloClient } from '@apollo/react-hooks';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBullseye,
  faShoePrints,
  faMagic,
  faTrashAlt,
  faStar,
} from '@fortawesome/free-solid-svg-icons';

import { useTranslation } from 'i18n';
import { itemCardStyle, blue6 } from 'common/mixins';
import { useDeleteItemMutation, checkAuthentication } from 'common/utils';
import { ItemStatsList } from 'common/wrappers';
import { customSet_customSetById_equippedItems } from 'graphql/queries/__generated__/customSet';
import { Stat } from '__generated__/globalTypes';
import setEquippedItemExoMutation from 'graphql/mutations/setEquippedItemExo.graphql';
import {
  setEquippedItemExo,
  setEquippedItemExoVariables,
} from 'graphql/mutations/__generated__/setEquippedItemExo';
import { customSet } from 'graphql/fragments/__generated__/customSet';

const quickMageStats = [
  {
    stat: Stat.AP,
    faIcon: faStar,
  },
  {
    stat: Stat.MP,
    faIcon: faShoePrints,
  },
  {
    stat: Stat.RANGE,
    faIcon: faBullseye,
  },
];

const ACTION_PADDING = 12;

const actionWrapper = {
  margin: -ACTION_PADDING,
  padding: ACTION_PADDING,
  transition: 'color 0.3s',
  [':hover']: { color: blue6 },
};

interface IProps {
  equippedItem: customSet_customSetById_equippedItems;
  itemSlotId: string;
  customSet: customSet;
  openMageModal: (e: React.MouseEvent<HTMLElement>) => void;
}

const EquippedItemCard: React.FC<IProps> = ({
  equippedItem,
  itemSlotId,
  customSet,
  openMageModal,
}) => {
  const { t } = useTranslation(['common', 'mage', 'stat']);

  const deleteItem = useDeleteItemMutation(itemSlotId, customSet);

  const [quickExo] = useMutation<
    setEquippedItemExo,
    setEquippedItemExoVariables
  >(setEquippedItemExoMutation, {
    optimisticResponse: ({ stat, hasStat }) => ({
      setEquippedItemExo: {
        equippedItem: {
          ...equippedItem,
          exos: hasStat
            ? [
                ...equippedItem.exos,
                { id: '0', stat, value: 1, __typename: 'EquippedItemExo' },
              ]
            : equippedItem.exos.filter(({ stat: exoStat }) => stat !== exoStat),
        },
        __typename: 'SetEquippedItemExo',
      },
    }),
  });

  const onDelete = React.useCallback(() => {
    deleteItem();
  }, [deleteItem]);

  const client = useApolloClient();

  const onQuickMage = React.useCallback(
    async (e: React.MouseEvent<HTMLDivElement>) => {
      e.stopPropagation();
      const { stat: statToExo } = e.currentTarget.dataset;
      const ok = await checkAuthentication(client, t, customSet);
      if (!ok) return;
      quickExo({
        variables: {
          stat: statToExo as Stat,
          equippedItemId: equippedItem.id,
          hasStat: !equippedItem.exos.some(({ stat }) => stat === statToExo),
        },
      });
    },
    [quickExo, equippedItem, client, customSet, t],
  );

  const quickMageMenu = quickMageStats.map(({ stat, faIcon }) => {
    const hasExo = equippedItem.exos.some(
      ({ stat: exoStat }) => stat === exoStat,
    );
    return (
      <Tooltip
        key={`quick-mage-${stat}`}
        title={t(hasExo ? 'REMOVE_EXO' : 'EXO', {
          ns: 'mage',
          stat: t(stat, { ns: 'stat' }),
        })}
        align={{ offset: [0, -ACTION_PADDING] }}
        placement="bottom"
      >
        <div
          css={{ color: hasExo ? blue6 : 'inherit', ...actionWrapper }}
          onClick={onQuickMage}
          data-stat={stat}
        >
          <FontAwesomeIcon icon={faIcon} data-stat={stat} />
        </div>
      </Tooltip>
    );
  });

  return (
    <Card
      size="small"
      css={css({
        ...itemCardStyle,
        display: 'flex',
        flexDirection: 'column',
        ['.ant-card-body']: {
          flex: '1',
        },
        border: 'none',
        borderRadius: 4,
        minWidth: 256,
      })}
      actions={[
        ...quickMageMenu,
        <Tooltip
          title={t('MAGE', { ns: 'mage' })}
          align={{ offset: [0, -ACTION_PADDING] }}
          placement="bottom"
        >
          <div css={actionWrapper} onClick={openMageModal}>
            <FontAwesomeIcon icon={faMagic} />
          </div>
        </Tooltip>,
        <Tooltip
          title={t('DELETE')}
          align={{ offset: [0, -ACTION_PADDING] }}
          placement="bottom"
        >
          <div css={actionWrapper} onClick={onDelete}>
            <FontAwesomeIcon icon={faTrashAlt} onClick={onDelete} />
          </div>
        </Tooltip>,
      ]}
    >
      <ItemStatsList
        item={equippedItem.item}
        css={{ paddingLeft: 16, marginBottom: 0 }}
        exos={equippedItem.exos}
      />
    </Card>
  );
};

export default EquippedItemCard;